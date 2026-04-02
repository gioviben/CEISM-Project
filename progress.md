# Progress — ST7: Virtual Seismic Site Imaging

Documentazione completa del progetto: teoria, struttura della repo, stato del codice, domande e risposte.

---

## 1. Obiettivo del progetto

Il progetto ha come obiettivo fare **imaging sismico del sottosuolo** tramite **Reverse Time Migration (RTM)** con metodo degli elementi spettrali (SEM3D).

Dato che hai registrato onde sismiche con dei sensori in superficie (`d_obs`), vuoi ricostruire le proprietà meccaniche del terreno sotto — i **parametri di Lamé**: λ (Lambda), μ (Mu) e la densità ρ.

**Obiettivo finale dichiarato**: implementare e parallelizzare il Conjugate Gradient (CG) su un cluster HPC (DCE di CentraleSupélec), usando MPI.

---

## 2. Background teorico

### 2.1 Il metodo degli Elementi Spettrali (SEM3D)

SEM3D è un solver Fortran/C++ per la simulazione della propagazione di onde elastiche in 3D, basato sul metodo degli elementi spettrali (SEM = Spectral Element Method):

- Il dominio 3D è discretizzato in una **mesh di esaedri** (cubetti deformati)
- In ogni elemento si usano punti di quadratura **GLL (Gauss-Lobatto-Legendre)**
- Il metodo di Galerkin porta all'equazione:

```
M·Ü + K(m)·U = F(t)
```

dove:
- `M` = matrice di massa (diagonale in SEM, grazie ai punti GLL)
- `K(m)` = matrice di rigidezza (dipende dal materiale m = λ,μ,ρ)
- `F(t)` = vettore delle forze (sorgente sismica)
- `U` = vettore degli spostamenti a tutti i nodi della mesh

### 2.2 Integrazione nel tempo: schema di Newmark

Per integrare nel tempo si usa lo **schema di Newmark**. Ad ogni timestep si risolve:

```
A · X = b

dove:
  A = M + β·Δt²·K(m)      ← matrice del sistema
  b = F_{n+1} + termini di storia temporale
  X = U_{n+1}              ← spostamento al passo successivo
```

Questo è un **sistema lineare** grande (milioni di gradi di libertà). Il Conjugate Gradient (CG) è il metodo iterativo usato per risolverlo.

### 2.3 Il campo di spostamento u(x,t)

`u(x,t)` **NON è scalare** — è un **campo vettoriale 3D**:

```
u(x,t) = [u_x(x,t),  u_y(x,t),  u_z(x,t)]
```

Per ogni punto `x = (x,y,z)` della mesh e ogni istante `t`, ci sono tre componenti che descrivono quanto si è spostato il terreno nelle direzioni x, y, z.

**Dimensioni concrete**:
```
u  →  shape: (N_nodi, 3, N_timestep)

esempio tipico:
  N_nodi     = 500.000
  N_timestep = 10.000
  → 500.000 × 3 × 10.000 × 8 bytes ≈ 120 GB
```

Ecco perché non si salva tutto in RAM — si usa checkpointing o si salvano solo gli snapshot a intervalli regolari.

I **dati osservati** `d_obs` sono molto più piccoli perché registrati solo ai ricevitori:
```
d_obs → shape: (N_ricevitori, 3, N_timestep)
```

### 2.4 Il tensore di deformazione ε[u]

Nel calcolo del gradiente appare `ε[u]` — il tensore di deformazione (symmetric gradient):

```
ε_ij = ½ (∂u_i/∂x_j + ∂u_j/∂x_i)
```

È un tensore 3×3 simmetrico → 6 componenti indipendenti: xx, yy, zz, xy, xz, yz.

Le due quantità usate nel gradiente:
- `tr(ε)  = ε_xx + ε_yy + ε_zz`  → dilatazione volumetrica (legata a λ)
- `dev(ε) = ε - ⅓·tr(ε)·I`        → deformazione di taglio (legata a μ)

In SEM3D: `evol` = volumetric strain = tr(ε), `edev` = deviatoric strain = dev(ε).

---

## 3. Il problema inverso: RTM

### 3.1 La funzione di costo (misfit)

```
J(m) = ½ · ‖u(m) - d_obs‖²   +   R(m)
         misfit ai ricevitori      regolarizzazione
```

dove `u(m)` è lo spostamento simulato con il materiale corrente `m`, e `d_obs` è quello osservato.

### 3.2 Perché serve il metodo dello stato aggiunto

Per minimizzare `J(m)` con gradient descent serve `∇_m J`. La derivata è:

```
∂J/∂m_i = Σ_j  (u_j - d_obs_j) · ∂u_j/∂m_i
```

Il termine `∂u_j/∂m_i` è la **Jacobiana**: quanto cambia lo spostamento al ricevitore `j` se perturbi il materiale nel punto `i`. Per calcolarla direttamente servirebbero **una simulazione per ogni parametro** — con milioni di parametri, impossibile.

**Il metodo dello stato aggiunto** calcola `∇J` con **una sola simulazione aggiuntiva**, indipendentemente dalla dimensione di `m`.

### 3.3 Il problema aggiunto: derivazione

Si definisce il **Lagrangiano**:
```
L(u, Λ, m) = J(u, m) + Λᵀ · [A(m)·u - b]
```

dove `Λ` è il moltiplicatore di Lagrange = **stato aggiunto** (adjoint wavefield).

Condizioni di stazionarietà:
- `∂L/∂Λ = 0` → problema forward: `A·u = b`
- `∂L/∂u = 0` → **problema aggiunto**: `Aᵀ·Λ = -(u - d_obs)`
- `∂L/∂m`     → **gradiente** (senza Jacobiana)

Poiché A è simmetrica (Newmark), `Aᵀ = A`:
```
A(m) · Λ = -(u - d_obs)   ← residui ai ricevitori come sorgenti
```

**Intuizione fisica**: stai "rispedendo indietro" le discrepanze tra simulazione e dati, come sorgenti dai sensori. Le onde aggionte `Λ(x,t)` si propagano all'indietro nel tempo (da T→0) e si concentrano nelle zone del modello che hanno causato gli errori — esattamente dove il gradiente è alto.

### 3.4 Il gradiente senza Jacobiana

```
g_λ(x) = ∂J/∂λ(x) = ∫₀ᵀ  tr(ε[u(x,t)]) · tr(ε[Λ(x,t)])  dt

g_μ(x) = ∂J/∂μ(x) = ∫₀ᵀ  dev(ε[u(x,t)]) : dev(ε[Λ(x,t)])  dt
```

Il gradiente in un punto `x` è la **correlazione temporale** tra la deformazione forward e quella aggiunta in quel punto. È grande dove entrambe le onde passano con energia.

---

## 4. L'algoritmo RTM completo

```
m_0 = materiale iniziale (stima)

for n in range(N_iterazioni):

    ─── STEP 1: Forward solve ─────────────────────────────────────
    Lancia SEM3D con materiale m_n
    → ottieni u(x,t) su tutto il dominio (snapshots)
    → ottieni u(x_ric, t) ai ricevitori (traces)

    ─── STEP 2: Misfit ────────────────────────────────────────────
    r(t) = u(x_ric, t) - d_obs(t)
    J_n  = ½ · ‖r‖²

    ─── STEP 3: Adjoint solve ─────────────────────────────────────
    Inietta r(T-t) come sorgenti ai ricevitori (time-reversed)
    Lancia SEM3D al contrario (t: T → 0)
    → ottieni Λ(x,t) su tutto il dominio

    ─── STEP 4: Gradiente ─────────────────────────────────────────
    g_λ(x) = ∫ tr(ε[u]) · tr(ε[Λ]) dt     (usa evol dai snapshot)
    g_μ(x) = ∫ dev(ε[u]) : dev(ε[Λ]) dt   (usa edev dai snapshot)

    ─── STEP 5: Direzione CG (Fletcher-Reeves) ────────────────────
    se n == 0:
        p_0 = -g_0
    else:
        β_n = ‖g_n‖² / ‖g_{n-1}‖²
        p_n = -g_n + β_n · p_{n-1}

    ─── STEP 6: Line search (backtracking Armijo) ─────────────────
    α = α_0
    while J(m_n + α·p_n) > J(m_n) + τ·α·(g_n·p_n):
        α = c · α    # riduci passo

    ─── STEP 7: Aggiornamento ─────────────────────────────────────
    m_{n+1} = m_n + α_n · p_n
    scrivi nuovi file HDF5 (example_la.h5, example_mu.h5)

    if ‖g_n‖ < ε: break

return m_N   ← modello ricostruito
```

### Perché CG invece di gradient descent?

Il gradient descent farebbe `m_{n+1} = m_n - α·g_n` ma "dimentica" le iterazioni precedenti e rimbalza. Il CG combina il gradiente attuale con la direzione precedente in modo **coniugato** (ortogonale nello spazio di Krylov) → converge molto più in fretta.

### La line search è costosa

Ogni valutazione di `J(m + α·p)` richiede un'intera simulazione forward (job SLURM sul cluster). Bisogna minimizzare il numero di valutazioni.

---

## 5. La parallelizzazione MPI

Il dominio 3D viene **decomposto tra i processi MPI**: ogni rank gestisce un sottodominio della mesh. L'output del mesher (`mesh4spec.0000.h5`, `mesh4spec.0001.h5`, ...) mostra questa decomposizione — un file per processo.

Operazioni da parallelizzare:
- **Moltiplicazione A·X**: locale per sottodominio + comunicazione dei bordi
- **Prodotti scalari** come `g·g` (usato nel CG): `MPI_Allreduce` su tutti i rank
- **Lettura snapshot**: già implementata in `parse_sem3d_snapshots.py` con MPI4py

Template MPI già presente nel codice:
```python
import mpi4py
mpi4py.rc.initialize = False
mpi4py.rc.finalize = False
from mpi4py import MPI

MPI.Init()
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# ogni rank lavora sul suo sottodominio...

# riduzione globale (es. per la norma del gradiente):
local_norm = np.dot(g_local, g_local)
global_norm = comm.allreduce(local_norm, op=MPI.SUM)

MPI.Finalize()
```

---

## 6. Struttura della repository

```
CEISM-Project/
├── slides-20260329/              ← TEORIA (PDF)
├── pysem/                        ← TOOLKIT Python (pre/post-processing)
├── tutorials_SEM3D_DCE/          ← ESEMPI GIÀ ESEGUITI (riferimento)
└── SEM3D_ST7_project2026_todo/   ← PROGETTO REALE (da completare)
```

---

## 7. Cartella: `slides-20260329/`

Contiene 5 PDF con tutta la teoria del progetto:

| File | Contenuto |
|------|-----------|
| `FG_FEM.pdf` (53 pag.) | Hamilton → Euler-Lagrange → FEM: mesh, funzioni di forma, Galerkin, assembly di M e K, quadratura GLL, schema di Newmark. Slides 40-41: `M·Ü + K·U = F → A·X = b` con CG |
| `ST7_Adjoint_State_Theory.pdf` (11 pag.) | Teoria probabilistica inversa → minimizzazione misfit → Lagrangiano → derivazione del problema aggiunto |
| `ST7_Reverse_Time_Migration_SEM3D.pdf` (28 pag.) | Setup RTM con PML → algoritmo RTM (slides 10-21): forward, misfit, adjoint, gradiente, problema di controllo, line search, pseudocodice iterativo a slide 20 |
| `ST7_SEM3D_tutorial.pdf` (26 pag.) | Uso pratico di SEM3D su HPC: module load, mesher, solver, SLURM, file di input, cartelle output |
| `ST7_Introduction.pdf` | Troppo grande (>20MB), non leggibile direttamente |

---

## 8. Cartella: `pysem/src/pysem/`

Il pacchetto Python installabile (`pip install -e .`). Tutto pre/post-processing — il solver è esterno.

### Pre-processing (creare input per SEM3D)

**`generate_h5_materials.py`**
- Crea file HDF5 delle proprietà del materiale: `prefix_la.h5`, `prefix_mu.h5`, `prefix_ds.h5`
- Funzione built-in: `linear_gradient(d, grd, nu=0.3)` — gradiente lineare lungo un asse
- Formula: `λ = (100 + 0.45·|z|)·10⁶ Pa`, `μ = 0.5·(1-2ν)/ν · λ`
- Scrive anche file XDMF per la visualizzazione in ParaView
- CLI: `generate-material @@tag linear_gradient @@pfx example @@dir z ...`

**`compute_pml_length.py`**
- Classe `pml`: calcola i parametri del PML (Perfectly Matched Layer) — boundary conditions assorbenti
- Dato il range di frequenze `[fl_min, fl_max]` e le velocità `cp`, `cs`:
  - Se conosci la lunghezza PML → calcola l'ampiezza `Ax`
  - Se conosci `Ax` → calcola la lunghezza PML necessaria
- Supporta due tipi: `PML` classico e `CPML` (Convolutional PML)

**`create_stations.py`**
- Genera griglia di ricevitori (file `stations.txt` con x,y,z per riga)

**`sem_stf.py`**
- Genera la Source Time Function (forma d'onda della sorgente):
  - `ricker(vtm, ts, wd)` — wavelet di Ricker
  - `gaussian(vtm, ts, wd)` — gaussiana
  - `spice_bench(vtm, ts, wd, k)` — funzione SPICE benchmark
- Output: file `.txt` con colonne `[t, STF(t)]`

**`mesh_shapes.py`**
- Primitive geometriche: `sphere(center, radius)`, `ellipsoid(center, axes)`
- Metodo `iswithin(points)` → maschera booleana per i punti dentro la forma
- Usato insieme a `modify_h5_materials.py`

**`modify_h5_materials.py`**
- Modifica file HDF5 di materiale applicando maschere spaziali
- Es: "dentro questa sfera, cambia λ a questo valore"

### Post-processing (leggere output di SEM3D)

**`parse_sem3d_snapshots.py`** ← modulo più pesante
- Legge i file HDF5 distribuiti degli snapshot del campo d'onda con MPI4py
- Classe `SnapshotsSEM3D`:
  - `GlobalReNumbering()`: ricostruisce la mesh globale unificando le mesh locali di ogni processo MPI tramite MD5 hashing delle coordinate dei nodi
  - `ParseSEM3DSnapshots()`: legge i campi statici una volta, poi itera sugli istanti temporali leggendo `Rsem{t}/sem_field.{proc}.h5`
- Dizionari chiave:
  - `typ`: classifica le variabili come `'static'` o `'dynamic'`
  - `sup`: classifica il supporto come `'node'` (nodi) o `'element'` (elementi)
- Variabili disponibili: `Displ` (spostamento), `Veloc`, `Accel`, `Stress` (6 comp.), `Strain` (6 comp.), `edev`, `evol`, `gradla`, `gradmu`
- Output: file VTU per ParaView

**`parse_sem3d_traces.py`**
- Legge le serie temporali dei ricevitori da `prot/Protection_XXXXX/Capteurs/capteurs.*.h5`
- Classe `SEM3DMonitor`: contiene la time-history per ogni monitor set
- `ParseSEM3DH5Traces()`: funzione principale — glob dei file HDF5, legge dataset `Variables`, costruisce dizionario ordinato
- Supporta filtraggio, decimazione, convoluzione via `scipy.signal`
- Questo modulo legge sia `d_obs` (dati osservati) che `u_sim` (simulazione corrente)

**`create_xmf_from_mesh.py`** + **`xdmf_help.py`**
- Creano file XDMF (metadata XML) che puntano agli HDF5 della mesh
- Usati per la visualizzazione in ParaView

### File di configurazione

**`pyproject.toml`**: definisce il pacchetto, Python ≥ 3.9, 6 entry point CLI
**`requirements.txt`**: dipendenze (h5py, numpy, scipy, mpi4py, tqdm, ...)

---

## 9. Cartella: `tutorials_SEM3D_DCE/`

Contiene **due simulazioni già eseguite** su cluster. Sono il riferimento per capire l'input/output reale.

### `tutorials_SEM3D_DCE/inputs/`
Template "puliti" da copiare:
- `input.spec` — config simulazione
- `mat.dat` — materiale binario legacy
- `mater.in` — proprietà fisiche: `S λ μ ρ Qp Qs` (S=solid)
- `stations.txt` — coordinate ricevitori

### `tutorials_SEM3D_DCE/tutorial1/` — Modello omogeneo
Simulazione più semplice, già eseguita. Contiene:
- **Input**: `input.spec` (6s, sorgente moment tensor `1 1 1 0 0 0`, Newmark α=0.5 β=-0.5)
- **Output del mesher**: 16 file `mesh4spec.0000.h5` ... `mesh4spec.0015.h5` (mesh decomposta in 16 processi MPI) + file XDMF per visualizzazione
- **Log**: `output.mesher`, `output.solver`
- **Job SLURM**: `MESHER.sbatch` (1 nodo, 1 task) e `SOLVER.sbatch` (1 nodo, 32 task MPI)

### `tutorials_SEM3D_DCE/tutorial2/` — Modello a gradiente lineare
Simulazione più complessa, già eseguita. Contiene:
- **Materiale generato**: `linear_gradient_la.h5`, `linear_gradient_mu.h5`, `linear_gradient_ds.h5` (output di `generate_h5_materials.py`)
- **STF**: `gaussian_stf.txt`
- **Output del solver**: `prot/Protection_00000867/Capteurs/capteurs.*.h5` ← i dati reali dei ricevitori

```
prot/Protection_00000867/Capteurs/
├── capteurs.0000.h5    ← time-series del proc. MPI 0 (displacement, velocity...)
├── capteurs.0003.h5    ← proc. MPI 3
├── ...                 ← solo i processi che contengono ricevitori
└── Stations_0_Displ_0.png    ← grafici già generati (componente x)
└── Stations_0_Displ_1.png    ← componente y
└── Stations_0_Displ_2.png    ← componente z
```

**Questi `capteurs.*.h5` sono i tuoi `d_obs`** — i dati osservati con il modello "vero" (gradiente lineare). Il problema inverso consiste nel ricostruire quel gradiente lineare partendo da un modello iniziale omogeneo.

---

## 10. Cartella: `SEM3D_ST7_project2026_todo/`

È il **template del progetto vero** — gli input sono già configurati per il problema RTM, ma il codice Python del loop di inversione non esiste ancora.

```
SEM3D_ST7_project2026_todo/
└── SEM3D_ST7_project2026_todo/
    ├── input.spec          ← config per il PROBLEMA REALE
    ├── mesh.input          ← 120 elementi, 1 dominio
    ├── material.spec       ← punta a "example_la.h5" / "example_mu.h5"
    ├── mater.in            ← 3 layer: S λ=2352 μ=1257 ρ=2000
    ├── mat.dat             ← binario legacy
    ├── gaussian_stf.txt    ← STF già generata
    ├── stations.txt        ← griglia densa di ricevitori (~100k punti a z=0)
    ├── MESHER.sbatch       ← job SLURM mesher (1 nodo)
    └── SOLVER.sbatch       ← job SLURM solver (32 task MPI)
```

### Il file `input.spec` del progetto è già configurato per RTM

Differenze chiave rispetto al tutorial:

```perl
sim_time = 20.0           # simulazione più lunga
fmax = 0.1                # frequenza massima
snap_interval = 0.5       # snapshot ogni 0.5s

capteurs "Uobs" {         # ricevitori chiamati "Uobs" = u osservato!
    type = points;
    file = "stations.txt";
    period = 68;           # campionamento ogni 68 timestep
};

pml_infos {               # PML configurato esplicitamente
    pml_type = CPML;
    cpml_kappa0 = 10.0;
    cpml_rc = 0.000000001;
};

out_variables {
    dis  = 1;   # displacement
    vel  = 1;   # velocity
    acc  = 1;   # acceleration
    edev = 1;   # deviatoric strain ← SERVE PER IL GRADIENTE g_μ
    evol = 1;   # volumetric strain ← SERVE PER IL GRADIENTE g_λ
    gradla = 1; # gradient Lambda ← CAMPO AUSILIARIO PER REGOLARIZZAZIONE
    gradmu = 1; # gradient Mu
};
```

### Le `stations.txt` del progetto

Griglia regolare in superficie (z=0) su dominio ~2200×2200 m:
```
-1100.00000 -1100.00000  0.00000
-1077.77778 -1100.00000  0.00000
...
```
Ricevitori tipici per RTM: distribuiti su tutta la superficie per massimizzare la copertura.

---

## 11. Cosa manca (da implementare)

Il loop RTM e il Conjugate Gradient devono essere scritti da zero. Il codice esistente fornisce solo l'infrastruttura.

### Flusso delle cartelle nel loop RTM

```
STEP 1 — Prepara m_0 (una volta sola)
  TOOL: generate_h5_materials.py
  INPUT: parametri del gradiente (xlim, zlim, step)
  OUTPUT: example_la.h5, example_mu.h5, example_ds.h5
  DESTINAZIONE: SEM3D_ST7_project2026_todo/

STEP 2 — Mesh (una volta sola)
  TOOL: sbatch MESHER.sbatch
  INPUT: mesh.input (120 elem, 1 dominio)
  OUTPUT: mesh4spec.*.h5 (decomposto per MPI)
  DESTINAZIONE: SEM3D_ST7_project2026_todo/sem/

STEP 3 — Forward solve [ogni iterazione]
  TOOL: sbatch SOLVER.sbatch
  INPUT: input.spec, material.spec → example_la/mu/ds.h5, stations.txt
  OUTPUT:
    prot/Protection_XXXXX/Capteurs/capteurs.*.h5  ← u_sim ai ricevitori
    res/Rsem*/sem_field.*.h5                       ← u(x,t) snapshots

STEP 4 — Misfit [Python da scrivere]
  TOOL: parse_sem3d_traces.py → leggi capteurs.*.h5
  CALCOLO: r(t) = u_sim(t) - d_obs(t)
  NOTA: d_obs viene da tutorials_SEM3D_DCE/tutorial2/prot/

STEP 5 — Adjoint solve [ogni iterazione]
  TOOL: scrivi r(T-t) come nuova STF ai ricevitori, sbatch SOLVER.sbatch
  INPUT: input.spec modificato con sorgenti agli "Uobs"
  OUTPUT: Lambda(x,t) snapshots

STEP 6 — Gradiente [Python da scrivere]
  TOOL: parse_sem3d_snapshots.py → leggi edev e evol di u e Λ
  CALCOLO:
    g_λ(x) = Σ_t  evol[u](x,t) · evol[Λ](x,t)
    g_μ(x) = Σ_t  edev[u](x,t) : edev[Λ](x,t)

STEP 7 — CG + line search + aggiornamento [Python da scrivere]
  CALCOLO: β, p_n, α (backtracking), m_{n+1}
  OUTPUT: aggiorna example_la.h5, example_mu.h5
  TOOL: generate_h5_materials.py o scrittura diretta HDF5

→ torna a STEP 3
```

### File Python da creare

```
pysem/src/pysem/
├── [ESISTE] tutti i moduli pre/post-processing
│
├── [DA CREARE] rtm_inversion.py
│     Loop principale RTM: orchestra forward, misfit, adjoint, gradiente, CG
│
├── [DA CREARE] conjugate_gradient.py
│     Solver CG parallelo MPI per A·X=b e per l'ottimizzazione
│
├── [DA CREARE] adjoint_source.py
│     Costruzione sorgenti aggiunto: scrivi r(T-t) nel formato SEM3D
│
└── [DA CREARE] gradient_compute.py
      Cross-correlazione temporale dei campi di deformazione forward e adjoint
```

---

## 12. Infrastruttura MPI disponibile

Il template MPI è già in `parse_sem3d_snapshots.py`:

```python
import mpi4py
mpi4py.rc.initialize = False   # lifecycle MPI gestito esternamente
mpi4py.rc.finalize = False
from mpi4py import MPI

MPI.Init()
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# distribuzione del lavoro tra rank:
files_per_rank = total_files // size
my_files = all_files[rank * files_per_rank : (rank+1) * files_per_rank]

# ogni rank lavora sul suo sottodominio...

# raccolta risultati (gather al rank 0):
all_results = comm.gather(local_result, root=0)

# riduzione globale (per prodotti scalari nel CG):
local_norm = np.dot(g_local, g_local)
global_norm = comm.allreduce(local_norm, op=MPI.SUM)

MPI.Finalize()
```

---

## 13. File di configurazione SEM3D: reference rapido

### `input.spec`
```perl
run_name = "nome";
sim_time = 20.0;           # durata simulazione [s]
mesh_file = "mesh4spec";   # prefisso file mesh
mat_file  = "material.input"; # o "material.spec"
ngll = 5;                  # ordine GLL (5 = 5×5×5 punti per elemento)
fmax = 0.1;                # frequenza massima [Hz]

source { coords = x y z; type = impulse; dir = 1 1 1; func = file; time_file = "stf.txt"; }
capteurs "nome" { type = points; file = "stations.txt"; period = N; }
time_scheme { veloc_scheme = true; alpha = 0.5; beta = 0.5; gamma = 1; courant = 0.2; }
pml_infos { pml_type = CPML; ... }
out_variables { dis=1; vel=1; acc=1; edev=1; evol=1; gradla=1; gradmu=1; }
```

### `material.spec`
```perl
material 0 {
    domain   = solid;
    deftype  = Lambda_Mu;
    spacedef = file;
    filename0 = "example_la.h5";   # λ
    filename1 = "example_mu.h5";   # μ
    filename2 = "example_ds.h5";   # ρ
};
material 3 { copy = 0; };  # copia le proprietà del materiale 0
```

### `mater.in`
```
3                           # numero di materiali
S 2352.84 1257.64 2000.0 1000.0 1000.0   # S=solid λ μ ρ Qp Qs
```

### `SOLVER.sbatch`
```bash
#SBATCH --nodes=1
#SBATCH --ntasks=32         # processi MPI
module load sem3d/2024.02.22/intel-2021.9.0-intel-oneapi-mpi
mpirun -n $SLURM_NTASKS sem3d.exe > output.solver
```

---

## 14. Formato output di SEM3D

### Traces (ricevitori)
```
prot/Protection_XXXXXXXX/Capteurs/capteurs.PPPP.h5
```
- Un file per ogni processo MPI `PPPP` che contiene almeno un ricevitore
- Struttura interna: dataset `Variables` (lista dei campi), poi un dataset per ogni campo/stazione
- Letto da: `parse_sem3d_traces.py` → `ParseSEM3DH5Traces()`

### Snapshots (campo intero)
```
res/Rsem{timestep}/sem_field.PPPP.h5
```
- Un file per ogni processo MPI `PPPP` per ogni timestep salvato
- Contiene: Displ, Veloc, Accel, Stress, Strain, edev, evol, gradla, gradmu...
- Letto da: `parse_sem3d_snapshots.py` → `ParseSEM3DSnapshots()`

---

## 15. Analisi teorica del gradiente (slide 17-18 + problema di controllo)

### Le formule esatte (slide 17)

Dalla slide 17 il gradiente di misfit è:

```
g_mis^λ = -∑_{n=0}^{N_T} ⊕_{e=1}^{N_e} ∫_{Ω_e} N(x) ε_vol,n(x) · ε^Λ_vol,n(x) dv Δt_n    (17)

g_mis^μ = -∑_{n=0}^{N_T} ⊕_{e=1}^{N_e} ∫_{Ω_e} N(x) (2ε_vol,n(x)·ε^Λ_vol,n(x) + ∑_{i,j} e_ij(x)·e^Λ_ij(x)) dv Δt_n    (18)
```

dove e_ij = componenti deviatoriche di ε (non la deviatorica intera — solo le 6 componenti).

Il problema di controllo (slide 15, eq. 14-15) è:
```
(1/ρ) M g_λ = R_λ g_reg^λ + g_mis^λ
(1/ρ) M g_μ = R_μ g_reg^μ + g_mis^μ
```

La matrice massa-like (slide 17, eq. 16):
```
(1/ρ) M = ⊕_{e=1}^{N_e} ∫_{Ω_e} N(x) N^T(x) dv
```

### Perché N(x) si cancella — derivazione dalle slide

**Passo 1 — Origine di N(x)**: dalla slide 15, λ(x) è parametrizzato come `λ|_{Ω_e}(x) = N^T(x) λ_e`. Quindi ∂λ(x)/∂λ_e = N(x), e per la chain rule:
```
g_mis^λ_e = ∫ [∂J/∂λ(x)] · N(x) dΩ
```
Ecco perché N(x) appare in eq. (17) — viene dalla parametrizzazione FEM.

**Passo 2 — Quadratura GLL (N_i(x_j) = δ_ij)**: in SEM i punti di integrazione GLL coincidono con i nodi delle funzioni di forma di Lagrange. La proprietà chiave:
```
∫_{Ω_e} N_i(x) · f(x) dv  ≈  ∑_j w_j J_j N_i(x_j) f(x_j) = w_i J_i f(x_i)
```
Solo il termine j=i sopravvive.

**Passo 3 — Calcolo esplicito delle due quantità**:
```
(1/ρ) M_ii  =  w_i · J_i                                               (dalla eq. 16)
g_mis^λ_i   =  -∑_n  w_i · J_i · ε_vol,n(i) · ε^Λ_vol,n(i) · Δt_n    (dalla eq. 17)
```

**Passo 4 — Soluzione del problema di controllo (eq. 14)**:
```
(w_i · J_i) · g_λ_i = -∑_n  w_i · J_i · ε_vol,n(i) · ε^Λ_vol,n(i) · Δt_n

Divido per (w_i · J_i):

g_λ_i = -∑_n  ε_vol,n(i) · ε^Λ_vol,n(i) · Δt_n
```

**Conclusione**: w_i·J_i è al denominatore (dalla matrice di massa) e al numeratore (da g_mis^λ). Si cancella esattamente perché entrambi provengono dallo stesso integrale con N(x). Il codice che calcola direttamente la cross-correlazione puntuale senza pesi è **corretto**.

### Bug trovati nel codice (gradient_compute.py)

**Bug 1 — Segno sbagliato (entrambi g_λ e g_μ)**:
- Codice originale: `g_lambda_local += ...` e `g_mu_local += ...`
- Corretto: `-=` (il segno meno è esplicito in entrambe le eq. 17 e 18)

**Bug 2 — Termine volumetrico mancante in g_μ**:
- Codice originale: `g_mu_local += dd * dt_snap` con solo il termine deviatorico
- Formula corretta (eq. 18): `2·ε_vol·ε^Λ_vol + ∑_{i,j} e_ij·e^Λ_ij`
- Il termine `2*evol_fwd*evol_adj` era completamente assente

**Correzione applicata (righe 261-269)**:
```python
# g_λ: cross-correlazione volumetrica — segno meno da eq. 17
g_lambda_local -= evol_fwd * evol_adj * dt_snap

# g_μ: eq. 18 — due termini: 2*vol*vol^Λ + dev:dev^Λ
# EDEV_WEIGHTS = [1,1,1,2,2,2] dà il fattore 2 agli off-diagonal (simmetria del tensore)
dd = np.sum(EDEV_WEIGHTS * edev_fwd * edev_adj, axis=1)
g_mu_local -= (2.0 * evol_fwd * evol_adj + dd) * dt_snap
```

### Cosa era già corretto

- **EDEV_WEIGHTS = [1,1,1,2,2,2]**: il prodotto doppio ∑_{i,j} e_ij·e^Λ_ij per un tensore simmetrico stored come [xx,yy,zz,xy,xz,yz] vale `xx*xx^Λ + yy*yy^Λ + zz*zz^Λ + 2*(xy*xy^Λ + xz*xz^Λ + yz*yz^Λ)` — il fattore 2 è corretto ✓
- **Allineamento temporale forward/adjoint**: `adj_snap = n_snap + 1 - k` ✓
- **Struttura MPI e Gatherv** ✓
- **Architettura senza pesi GLL espliciti** ✓ (si cancellano come dimostrato sopra)

---

## 16. Stato attuale del progetto

| Componente | Stato |
|---|---|
| Teoria (PDF) | Completa |
| Toolkit pre-processing Python | Completo |
| Toolkit post-processing Python | Completo |
| Infrastruttura MPI | Presente (in parse_sem3d_snapshots.py) |
| Esempi eseguiti (tutorial1, tutorial2) | Completi con output |
| Input del progetto reale | Configurato (input.spec, stations.txt, STF) |
| Calcolo gradiente da snapshot | **Implementato e corretto** (gradient_compute.py) |
| Loop RTM in Python | **DA IMPLEMENTARE** |
| Conjugate Gradient parallelo | **DA IMPLEMENTARE** |
| Scrittura sorgenti aggiunto | **DA IMPLEMENTARE** |
| Line search | **DA IMPLEMENTARE** |