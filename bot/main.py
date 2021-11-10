from modules import *

# Clear the screen for a fresh start
os.system('cls' if os.name == 'nt' else 'clear')

# Program will automatically close if required files are not found
# Handled in readData() function

driver = initalizeDriver()

finalResult = list()

try:
    objects = readData()
    if len(objects):
        # Visit Cargo Website
        driver.get("https://cargo.build/")
        waitForLogin()
        for o in objects:
            error = False
            errorValue = None
            try:
                url = o.get('url', None)
                price = o.get('price', None)
                ethAddress = o.get('ethAddress', None)
                royalties = o.get('royalties', None)
                if url and price and ethAddress and royalties:
                    scarpe(driver, url, price, ethAddress, royalties)
            except Exception as e:
                error = True
                errorValue = traceback.format_exc()
            finally:
                o.update({'status': 'OK' if not error else 'NOT OK'})
                o.update({'timestamp': datetime.now().strftime("%d/%m/%Y %H:%M:%S")})
                o.update({'error': errorValue})
                finalResult.append(o)
                print(f"Status: {'OK' if not error else 'Not OK'}")
            print("-------------------------------------------------")
        print("Operation completed successfully!")
except Exception as e:
    print(e)
    # print(traceback.format_exc())
    print("There was a general error.")
finally:
    print("Thankyou for using the bot today.")
    writeData(finalResult)
    # driver.quit()
    raise SystemExit