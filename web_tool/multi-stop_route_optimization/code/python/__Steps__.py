# =============================================================================
# asp.net user request logic
# =============================================================================
# 1. user request
# 2. assign random request ID
# 3. asp.net create folder with user ID and write input files to the folder
# 4. asp.net log request - __queue__.txt file - task_computer (1,2,3...), request_ID, email, input_variables
# 5. continously check if __initiated__.txt file is in the request_ID folder.  
# 6. update task___queue__.txt file - delete every completed request_ID
# 7. if yes in 5, continously check if __completed__.txt is in the request_ID folder.  
# 8. if yes in 6, update message to user. 



# =============================================================================
# asp.net server api process logic - runs with page load
# =============================================================================
# 1. read address ?status=initiated&request_ID=XXXXX     
# 2. write file __initiated__.txt to the request_ID folder

# 1. read address ?maintenance=day
# 2. if the key is maintenance, delete old folders and files - maybe keep only 1 day


# =============================================================================
# python logic
# =============================================================================
# 1. continously check if there is any user request in task queue. - __queue__.txt file in the server
# 2. if yes in 2, check the folder by request ID - the request_ID folder in the server
# 3. send notificiation to the server - the server will write file __initiated__.txt to the request_ID folder
# 4. run application
# 5. send notificiation to the server - the server will write file __completed__.txt to the request_ID folder
# 6. log the request and complete status
# 7. update previous request_ID list
# 8. go back to 1 and check another request
