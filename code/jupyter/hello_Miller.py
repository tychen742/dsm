# ##### writing a file
# ### file handling can be error-prone so we use try statement
# ### to handle exceptions  

# ##### open(), write(), close() #####
file = open('02_file1_write_hello_Miller.txt', 'w')   # 'w': write mode
try:
    file.write('hello world')
finally:
    file.close()
