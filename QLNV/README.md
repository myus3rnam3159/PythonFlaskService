# Cách debug python file  
https://towardsdatascience.com/how-to-debug-flask-applications-in-vs-code-c65c9bdbef21  

# Lỗi view function trong flask: https://stackoverflow.com/questions/55728457/flask-typeerror-the-view-function-did-not-return-a-valid-response-the-functio  

# jwt: https://flask-jwt-extended.readthedocs.io/en/stable/basic_usage/  

# Kiểm tra đúng môi trường ảo virtualenv của folder tương mới được chạy  

# Với pymongo arregate dùng pipeline thay cho  param
    *Docs: https://pymongo.readthedocs.io/en/stable/examples/aggregation.html

# pymongo chỉ hổ trợ query nhưng không hỗ trợ exclude fields bên trong nó, chỉ có thể read và field ở tầng ứng dụng  
    * Docs: https://pymongo.readthedocs.io/en/stable/tutorial.html

# Luyện tập config jwt trong file .ini , chú ý thuật toán hash đã có default value

# Option trong file config của Flask app  
    1. app: https://flask.palletsprojects.com/en/2.1.x/config/#configuration-basics  
    2. jwt: https://flask-jwt-extended.readthedocs.io/en/stable/options/#configuration-options  

# Khai báo tham số chỉ được 1 trong 2 loại: có default value hết hoặc non-default value hết  
    * Tham khảo: https://stackoverflow.com/questions/24719368/syntaxerror-non-default-argument-follows-default-argument  
# Doc pymongo: https://pymongo.readthedocs.io/  
    * Search kĩ sẽ ra  
# Luôn luôn check type trong python  
    * Câu lệnh: type(variable)  
# Hàm trong class lúc nào cũng phải có tham số self  
# Tạo môi trường ảo cho python project  
    1. cd vào folder chứa project, gõ cầu lệnh: virtualenv -p Đường-Dẫn-Tới-Thư-Mục-Cài-Python3\python.exe <tên folder chứa môi trường ảo>  
    2. Activate môt trường ảo (windows): <tên folder môi trường ảo>\Scripts\activate  
    3. Muốn deactivate, gõ lệnh: deactivate  
# Install package  
    1. Kiểm tra đã có package chưa: pip show <tên package>  
    2. Vào folder có file cần import package 
    3. Gõ lệnh: pip install <tên package>  
# Tham khảo  
    1. Convert to datetime trong python: https://stackoverflow.com/questions/41999094/how-to-insert-datetime-string-into-mongodb-as-isodate-using-pymongo  

    2. Convert cursor trả về từ pymongo thành json object: https://pinoria.com/how-to-fix-typeerror-objectid-is-not-json-serializable-with-pymongo/  

    3. Check type của biến trên python: https://pytutorial.com/python-check-variable-type  

    4. Lấy header response trong Flask: https://stackoverflow.com/questions/29386995/how-to-get-http-headers-in-flask  

    5. Convert kiểu date trả về từ mongo: https://www.mongodb.com/docs/manual/reference/operator/aggregation/dateToString/  

    6. Filter với project trong mongo aggregate: https://www.mongodb.com/docs/manual/reference/operator/aggregation/project/#mongodb-pipeline-pipe.-project  

    7. Set thời hạn cho jwt:  https://stackoverflow.com/questions/67998405/in-flask-jwt-extended-how-to-set-a-custom-token-expiry-time  

    8. Insert date vào mongodb dùng kiểu dữ diệu json: https://stackoverflow.com/questions/26901294/how-to-insert-date-into-mongo-from-json-file  

    9. Lấy thời gian hiện tại trong typescript: https://www.delftstack.com/howto/typescript/typescript-current-date/  

    10. Set namespace trong redis với python: https://stackoverflow.com/questions/29158618/redis-namespace  

    11. Gọi api từ api trong flask: https://stackoverflow.com/questions/59549527/calling-rest-api-of-a-flask-app-from-another-flask-app  

    12. Lấy param từ get request: https://stackoverflow.com/questions/24892035/how-can-i-get-the-named-parameters-from-a-url-using-flask  

    13. Convert response của hàm requests trong python thành json: https://grabthiscode.com/python/python-convert-requests-response-to-json  

    14. python redis client: https://docs.redis.com/latest/rs/references/client_references/client_python/  

    15. Làm tròn chữ số thập phân trong python: https://stackoverflow.com/questions/43147237/how-to-set-a-float-to-a-certain-number-of-decimal-places-in-python  

    16. Tính khoảng cách giữa 2 mốc thời gian ở dạng iso string: https://stackoverflow.com/questions/68566333/calculate-time-difference-between-two-times-using-iso-8601  

    17. Time format dùng để convert kiểu datetime trong python(dùng được với cả strptime và strftime):  
    https://www.geeksforgeeks.org/python-datetime-strptime-function/  
    https://stackoverflow.com/questions/33810980/date-time-split-in-python

    18. Parse time string thành datetime trong python: https://stackoverflow.com/questions/969285/
    how-do-i-translate-an-iso-8601-datetime-string-into-a-python-datetime-object    

    19. Insert isodate với pymongo: https://stackoverflow.com/questions/41999094/how-to-insert-datetime-string-into-mongodb-as-isodate-using-pymongo

    20. Xóa key trong pythond dic: https://datagy.io/python-delete-dictionary-key/  

    21. Cú pháp update một document trong mongo: https://www.mongodb.com/docs/manual/reference/method/db.collection.updateOne/#mongodb-method-db.collection.updateOne  

    22. Lấy độ dài của cursor trả về từ pymongo.find: https://www.geeksforgeeks.org/how-to-check-if-the-pymongo-cursor-is-empty/  

    23. In xuống dòng trong python: https://www.delftstack.com/howto/python/python-print-line-break/  

    24. Copy không clone dictionary trong python: https://stackoverflow.com/questions/8771808/copy-a-dictionary-into-a-new-variable-without-maintaining-the-link-with-previous  

    25. Lưu json vào redis thuần, nếu dùng set thay cho hset thì chỉ cần 2 argument: 
        https://stackoverflow.com/questions/66350291/how-to-create-a-column-and-set-key-and-value-to-redis-using-python   
        https://stackoverflow.com/questions/47078447/how-to-store-a-complex-nested-json-in-redis-using-python  
    
    26. Chuyển byte sang string (bỏ repr): https://stackoverflow.com/questions/49184578/how-to-convert-bytes-type-to-dictionary  

    27. Khi nào dùng pipe và subcribe trong angular: https://stackoverflow.com/questions/61309145/pipe-vs-subscribe-in-angular  

    28. Check null trong typescript: https://bobbyhadz.com/blog/typescript-check-if-null  

    29. Sử dụng boolean value với python redis: https://github.com/Onelinerhub/onelinerhub/blob/main/python-redis/how-to-use-boolean-values-in-redis.md

# ANGULAR
    1. sửa lỗi no provider for HttpClient: https://stackoverflow.com/questions/47236963/no-provider-for-httpclient  

    2. set header cho request: https://stackoverflow.com/questions/58834437/how-to-pass-authorization-header-token-in-api-call-in-angular  

    3. Khi gọi http post bắt buộc phải subcribe:  https://stackoverflow.com/questions/36208732/angular-2-http-post-is-not-sending-the-request#36208752  

    4. Cách debug angular app: https://stackoverflow.com/questions/42495655/how-to-debug-angular-with-vscode  