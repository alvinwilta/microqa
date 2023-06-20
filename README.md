# Microservice Quality Assesment

## Credits

built using callGraph from [koknat/callGraph](https://github.com/koknat/callGraph)

microservice examples used:

- robot-shop: https://github.com/instana/robot-shop
- tns: https://github.com/peterbourgon/tns

## Running

Run the script with makefile

```bash
cd src/

make all
```

there is a github action example on microqa.yml

## Documentations

configured with microqa-config.yaml

Optional Flags:

```
Determining the path of the config file:

--config <config filepath>
```

- [x] Finish ingraph
- [x] Test dot file for graph
- [ ] Test API for graph
- [x] Manage perl to execute callgraph, make a script to install perl

# Error Codes

Error codes are 2 digit errors. The first digit indicates the module where the error occurs and the second is the indication of the error. Below are the known errors:

| Error code | Module        | Reason                                                                                  |
| ---------- | ------------- | --------------------------------------------------------------------------------------- |
| 11         | Main          | Unknown service_connection_source read from configuration file for the 'file' argument  |
| 12         | Main          | Unknown service_connection_type read from configuration file for the 'api' argument     |
| 21         | Rule          | Invoked rule is not yet implemented or calculate() not yet implemented                  |
| 22         | Rule          | Involed rule is not yet implemented or setup_param() not yet implemented                |
| 23         | Rule          | Rule's 'best' parameter must be either 'left' or 'right'                                |
| 31         | Service Graph | Invalid file type for file defined in service_connection_filename argument (.dot file)  |
| 32         | Service Graph | Invalid file type for file defined in service_connection_filename argument (.json file) |
| 33         | Service Graph | Invalid weavescope json file                                                            |
| 34         | Service Graph | Weavescope API not connected                                                            |

# Other useful commands:

## Run via docker

```bash
docker run -v "<source code dir>:/app/<repo dir based on config>" -v "<config filepath>:/app/<config filename>" -v "<weavescope json filepath>:/app/<json filepath>" --network=host microqa
```

the json filepath volume is optional, only provide the path if you used the json file.

the network flag is optional, only provide the flag if you need to access host network.

e.g.

```bash
docker run -v "/home/alvinwilta/Documents/kuliah/Tugas Akhir/2_codes/robot-shop/:/app/robot-shop/" -v "./microqa-config.yaml:/app microqa-config.yaml" -v "./net_graph.json:/app/net_graph.json" microqa
```

or

```bash
docker run -v "/home/alvinwilta/Documents/kuliah/Tugas Akhir/2_codes/robot-shop/:/app/robot-shop/" -v "./microqa-config.yaml:/app microqa-config.yaml" --network=host microqa
```

## Running CallGraph independentlu

```
./callGraph <dir> -language <lang> -output <output file>
```

## Convert dot to png

```
dot -Tpng <filename>.dot -o <outputfile>.png
```

## Building the dockerfile

```
docker build -t alvinwilta/microqa src/
```
