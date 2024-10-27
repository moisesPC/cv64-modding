# Castlevania 64 Modding

This is a modding framework that allows you to inject C code, MIPS assembly, as well as any other file into Castlevania 64.

At the moment, it only supports the USA v1.0 version of the game</br>
(`sha1: 989A28782ED6B0BC489A1BBBD7BEC355D8F2707E`)

## Requirements
* Make
* Python 3.x and pip
* [armips](https://github.com/Kingcom/armips)
* [n64chain](https://github.com/tj90241/n64chain)

### Prerequisites
After installing, you need to add `armips` and `n64chain` exectuable directories to your system's PATH.

#### Linux
1. Open a terminal and input the following command to permanently add the `armips` and `n64chain` directories to PATH:
```
echo 'export PATH=$PATH:/path/to/armips:/path/to/n64chain/bin' >> ~/.bashrc && source ~/.bashrc
```

#### Windows

1. Press Win + X and select "System".
2. Click on "Advanced system settings" on the right.
3. Click the "Environment Variables" button.
4. Under "System variables", find and select the "Path" variable, then click "Edit".
5. Click "New" and add the full path to the directory containing the `armips` executable.
6. Click "New" again and add the full path to the `n64chain/bin` directory.
7. Click "OK" to close all dialogs.
8. Restart any open command prompts for the changes to take effect.

Verify the installation by opening a new terminal and running:

```
armips --version
mips64-elf-gcc --version
```

You will also need the `numba` and `numpy` python packages:
```
pip install numpy
pip install numba
```

## Building
Place a Castlevania 64 (USA v1.0) ROM in the root of the repository, and name it `cv64.z64`.

Then, write `make` to build the output ROM, and `make clean` to clean the build artifacts.

The names of the input and output ROMs can be modified in the `Makefile`.

## Documentation
Documentation for this project can be found [here](docs/index.md).
