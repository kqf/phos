## Merge the train output
The trains don't merge the output properly therefore it's necessary to do it manually. This set of scripts should be used to download, merge and upload back the analysis results


## Usage
Don't pass any arguments as it complicates all the macro. 

```bash
# Download from the merged lists
make download


# Upload to the local alien folder
make upload


# Run the entire sequence
make
```