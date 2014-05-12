
resultsFile = open('TopTenIPResult', 'w+')
for num in range(1, 10):
    resultsFile.write(str(num) + '\n')
    
resultsFile.close()
