# Microservice Quality Assesment

built using callGraph from [koknat/callGraph](https://github.com/koknat/callGraph)

configured with microqa-config.yaml

microservice examples used:

- robot-shop: https://github.com/instana/robot-shop
- tns: https://github.com/peterbourgon/tns

- [x] Finish ingraph
- [ ] Test API and dot file for graph
- [x] Manage perl to execute callgraph, make a script to install perl

# Error Code Documentation

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

```
./callGraph <dir> -language <lang> -output <output file>
```

convert dot to png

```
dot -Tpng <filename>.dot -o <outputfile>.png
```
