# Py_SBeLT

Rivers transport sediment particles. Individual particles can exhibit transport behavior that differs significantly when compared to other particles. py_SBeLT provides a simple Python framework to numerically examine how individual particle motions in rivers combine to produce rates of transport that can be measured at one of a number of downstream points. The model can be used for basic research, and the model's relatively straightforward set-up makes it an effective and efficient teaching tool to help students build intuition about river transport of sediment particles.

## Installation

First, [clone the Py_SBeLT repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) in a desired location.

Then install the required Python dependancies:

```bash
 pip3 install -r requirements.txt
```

## Nomeculture

- **Stream**: An 2D (x,y) area/domain consisting of bed particles and model particles. The length of the stream is set via parameters while the height has no explicit value. The left-most point of the stream is considered the upstram boundary while the right-most is considered the downstream boundary.
- **Bed Particle**: A fixed particle comprising the stream bed. At no point in the model simulation do bed particles move. Bed particles represent the lowest elevation in the stream.
- **Model Particle**: A particle subject to entrainment events. These particles move and have their location and other metrics tracked per-iteration for the duration of the model simulation.
- **Supporting Particle**: Particle that hold up other particles (i.e in a stack of 3 particles, the bottom two particles are supporting the top). Both bed and model particles can also be considered supporting particles at a given point in the model simulation.
- **Event Particle**: A model which has been selected to undergo an entrainment event. Only model particles can be considered event particles.
- **Available Vertex**: A horizontal location in the stream which a model particle is permitted to rest/land.
- **Desired Hop**: The place in the stream bed an event particle is assigned to move to based on random sampling informed by parameters.

## Parameters

The model reads in parameters from a yaml file. The default parameters file for the model is `param.yaml`, located in the **`model/parameters/`** directory:

```
project
│   README.md
│   requirements.txt
└───model
|   └───parameters
│   │   |   param.yaml
|   |   |   schema.yaml
│   │   run.py
│   │   ...
```

These parameters can be changed for whatever type of run you desire! However, all parameters have data type requirements and some have minimum and maximum permitted values. The parameters are validated at the start of the run and any incompatible entries will cause an error and error message to be raised. The following is a table of the parameters:

| Parameter | Type |Description |
| ----------- | ------- | ----------- |
| pack_density | float | The packing density of the model particles |
| x_max | int |Length of the domain in the streamwise direction (mm) |
| set_diam | float |Grain diameter (mm) |
| num_subregions | int | The number of bed subregions |
| level_limit | int | The maximum number of levels permitted (i.e how many particles high to stack)  |
| n_iterations | int | The number of iterations to run |
| lambda_1 | float | Lamba for poisson dist., used to determine the number of entrainment events |
| normal_dist | boolean |Flag for which distribution to sample from for hop calculations. True=Normal, False=logNormal |
| mu | float |Mean/expectation of the logNormal/Normal distribution for hop calculations |
| sigma | float |Standard deviation of logNormal/Normal distribution for hop calculations|
| data_save_interval | int | How often to record model particle arrays (e.g 1=save every iteration, 2=save every other) |
| height_dependancy | boolean | Flag indicating whether model automatically entrains particles that are at the height limit |
| filename_prefix | strong | Prefix for output filenames |

## Running the Model

1. Set current directory to **`py_SBeLT/model`**:

```bash
 cd /path/to/BeRCM/model
```

2. 
    a. Run a _single_ instance of the model:

    ```bash
    python3 run.py PATH_TO_PARAM_FILE
    ```

    Where `PATH_TO_PARAM_FILE` is the path to the desired parameters file. To use the default parameters file set `PARAM_FILE=`**`parameters/param.yaml`**.

    b. Run _multiple_ instances (not parallel, just multiple processes) of the model:

    ```bash
    python3 run_multiple.py NUM_PROCESSES PARAM_FILE...
    ```

    Note that multiple parameter files can be passed to the **`run_multiple.py`** script. If more than one parameter file is passed then the number of files passed must be equal to the number of processes requested. If only one is passed, then that one file is used by all processes.

## Results

All relevant information from the run is stored in an HDF5 file in the **`output/`** directory:

```
RCM_BedloadTransport
│   README.md
│   requirements.txt
└───model
│   └───output <--- here!
|   |   ...
```

Each run will have a unique filename based on the following syntax: `filename_prefix-YYMM-DDHH`, where `YYMM-DDHH` represents the time the simulation was started and `filename-prefix` is a string given in the `param.yaml` file. For example, a run started on December 24th, 2030 at 12:01pm and assigned the prefix hello-river will use the filename:

- **`hello-river-3012-2412.hdf5`**

Each HDF5 file will contain: the parameters used, the bed particle array, and initial model particle array. Then for each iteration the model particle arrays and event particles. Finally the particle flux list and the particle age and age range lists.

Each of these data values can be retrieved by opening the HDF5 file using [h5py](https://docs.h5py.org/en/stable/) and using the appropriate keys as shown below:

```{python3}
with h5py.File('hello-river-3012-2412.hdf5', 'r') as f:
    f["params"]["..param name..."][()]                              # parameters
    np.array(f["initial_values"]["bed"])                            # bed particles
    np.array(f["iteration_i"]["model"])                             # model p at end of iter i
    np.array(f["iteration_i"]["event_ids"])                         # events ids for iter i
    np.array(f["final_metrics"]["subregions"]["subregion-i-flux"])  # flux list
    np.array(f["final_metrics"]["avg_age"])                         # avg age list
    np.array(f["final_metrics"]["age_range"])                       # age range list
```

## Plotting

The project currently contains logic for plotting a visual of the streambed, a .gif of the streambed, the particle flux distribution, and particle age-related information.

Navigate to the **`plots/`** directory. Choose a desired HDF5 file to plot, name of the subfoler to save the plots into, and decide what range of iterations to plot for the streambed. Then run the following command:

```{bash}
python3 plot_maker.py PATH_TO_HDF5_FILE OUTPUT_NAME MIN_ITER MAX_ITER
```

For example, if you wanted to plot iterations 100 to 1000 from the **`hello-river-3012-2412.hdf5`** run in a directory named `hello-river-run` the command would be:

```{bash}
python3 plot_maker.py ../model/output/hello-river-3012-2412.hdf5 hello-river-run 100 1000
```

<!-- Embed a gif here as an example/motivation -->
