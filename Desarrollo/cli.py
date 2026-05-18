def main():
    while True:
        try:
            #
            output = input("copia algo")
            if output =="cerrar":
                return
        except KeyboardInterrupt:
            return

if __name__ == "__main__":
    main()