class Logger:
    _file = "data_processing_log"

    def log(str):
        print(str, flush=True)
        with open(Logger._file, "a") as fd:
            print(str, file=fd, flush=True)
            

