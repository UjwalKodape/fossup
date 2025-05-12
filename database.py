import pymysql as pm 

class Database:
    def __init__(self):
        self.con = pm.connect(host='localhost',user='root',password='root',database='fossup',port=3307)
        
#SIGNUP------------------------------------------------------------------------------------------------------------------------------------
    def storeuser(self, uname, email, pass1):
        self.cursor = self.con.cursor()
        a1=0
        a='active'
        sql = "INSERT INTO users (username, email, password) VALUES (%s,%s,%s);"
        var = (uname,email,pass1)
        self.cursor.execute(sql,var)

        try:
            self.con.commit()
            self.status = True
            self.cursor.close()
            return self.status
        except:
            self.con.rollback()
            self.status=False
            self.cursor.close()
            return self.status
        return self.status
#LOGIN---------------------------------------------------------------------------------------------------------------------------------------
    def checkUser(self ,username,pass11):
        self.cursor = self.con.cursor()
        sql = "SELECT * FROM users WHERE username = %s AND password = %s"
        var = (username, pass11)
        self.cursor.execute(sql,var)
        self.results = self.cursor.fetchone()
        print(self.results)
        print(self.results[0])
        self.id = self.results[0]
        if self.cursor.rowcount == 1:
            self.status = True
            print(self.status)
            self.cursor.close()
            return self.status,self.id  
        else:
            self.status = False
            print(self.status)
            self.cursor.close()
            return self.status,self.id

#MODERATOR-LOGIN---------------------------------------------------------------------------------------------------------------------------
    def checkMod(self ,name ,pass1):
        self.cursor = self.con.cursor()
        sql = "SELECT * FROM moderators WHERE name = %s AND password = %s"
        var = (name, pass1)
        self.cursor.execute(sql,var)
        self.results = self.cursor.fetchone()
        if self.cursor.rowcount == 1:
            status = True
            print(status)
            self.cursor.close()
            return status   
        else:
            status = False
            print(status)
            self.cursor.close()
            return status
#UPLOAD-BLOG------------------------------------------------------------------------------------------------------------------------------
    
    # def file_uplod(self,author_name, date, caption, description, image_path):
    def file_uplod(self,author_name, date, caption, description, image_path):
        self.cursor = self.con.cursor()
        # cursor = db.cursor()
        img = "None"
        sql = "INSERT INTO blogs (author_name, date, caption, description, image_path) VALUES (%s, %s, %s, %s, %s);"
        var = (author_name, date, caption, description, image_path)
        self.cursor.execute(sql,var)
        print("2")
        try:
            self.con.commit()
            self.status = True
            print("3")
            print(self.status)
            self.cursor.close()
            return self.status    
        except:
            self.con.rollback()
            self.status = False
            print(self.status)
            print("4")
            self.cursor.close()
            return self.status    
        # finally:
        #     print("5")
        #     self.cursor.close()  # Ensure the cursor is always closed
    
    def img_path_up(self,image_path, author_name):
        self.cursor = self.con.cursor()
        sql = "UPDATE blogs set image_path = %s WHERE author_name = %s"
        var = (image_path, author_name)
        self.cursor.execute(sql,var)
        print("2")
        try:
            self.con.commit()
            self.status = True
            print("3")
            print(self.status)
            self.cursor.close()
            return self.status    
        except:
            self.con.rollback()
            self.status = False
            print(self.status)
            print("4")
            self.cursor.close()
            return self.status    

#RETRIVING DATA-------------------------------------------------------------------------------------------------------------------        

    def all_data(self): 
        self.cursor = self.con.cursor()         # Creating the cursor object 
        sql = "SELECT * FROM blogs"
        self.cursor.execute(sql)                # Executing the SQL queries 
        # Printing the results
        self.results = self.cursor.fetchall()
        self.cursor.close()
        return self.results
    
    def users(self):
        self.cursor = self.con.cursor()         # Creating the cursor object 
        sql = "SELECT * FROM users"
        self.cursor.execute(sql)                # Executing the SQL queries 
        # Printing the results
        self.results = self.cursor.fetchall()
        self.cursor.close()
        return self.results
    
    def storeMod(self, name,email,phone,password):
        self.cursor = self.con.cursor()
        
        sql = "INSERT INTO moderators (name, email,phone, password) VALUES (%s,%s,%s,%s);"
        var = (name,email,phone,password)
        self.cursor.execute(sql,var)

        try:
            self.con.commit()
            self.status = True
            self.cursor.close()
            return self.status
        except:
            self.con.rollback()
            self.status=False
            self.cursor.close()
            return self.status
        
    def moderators(self):
        self.cursor = self.con.cursor()         # Creating the cursor object 
        sql = "SELECT * FROM moderators"
        self.cursor.execute(sql)                # Executing the SQL queries 
        # Printing the results
        self.results = self.cursor.fetchall()
        self.cursor.close()
        return self.results
    
#PAGE-OPERATIONS-------------------------------------------------------------------------------------------------------------------------
    def pageData(self, name,email,phone_number,address):
        self.cursor = self.con.cursor()
        sql = "INSERT INTO pageData (name, email,phone_number, address) VALUES (%s,%s,%s,%s);"
        var = (name,email,phone_number,address)
        self.cursor.execute(sql,var)

        try:
            self.con.commit()
            self.status = True
            self.cursor.close()
            return self.status
        except:
            self.con.rollback()
            self.status=False
            self.cursor.close()
            return self.status
        
    def pageUpdate(self):
        self.cursor = self.con.cursor()         # Creating the cursor object 
        sql = "SELECT * FROM pageData"
        self.cursor.execute(sql)                # Executing the SQL queries 
        # Printing the results
        self.results = self.cursor.fetchall()
        self.cursor.close()
        return self.results
    
#COUNT---------------------------------------------------------------------------------------------------------------------------------------
    def count_users(self):
        self.cursor = self.con.cursor()  # Creating the cursor object
        sql = "SELECT COUNT(*) FROM users"
        self.cursor.execute(sql)          # Execute the query
        result = self.cursor.fetchone()  # fetch one tuple
        self.cursor.close()              # Close the cursor
        if result:
            return result[0]             # return count value (first element)
        else:
            return 0   
        
    def count_blogs(self):
        self.cursor = self.con.cursor()  # Creating the cursor object
        sql = "SELECT COUNT(*) FROM blogs "  # Adjusted SQL query to filter by user_id
        self.cursor.execute(sql)  # Execute the query with the user_id parameter
        result = self.cursor.fetchone()  # fetch one tuple
        self.cursor.close()  # Close the cursor
        if result:
            return result[0]  # return count value (first element)
        else:
            return 0
        
    def upDateBlogStatus(self,id):
        self.cursor = self.con.cursor()
        sql = "update blogs set status = 1 where id ='%s'" % (id)
        self.cursor.execute(sql)
        self.con.commit  

    def count_likes(self,id):
        self.cursor = self.con.cursor()  # Creating the cursor object
        sql = "SELECT COUNT(*) FROM blogs WHERE u_id = %s"
        self.cursor.execute(sql,id)          # Execute the query
        result = self.cursor.fetchone()  # fetch one tuple
        self.cursor.close()              # Close the cursor
        if result:
            return result[0]             # return count value (first element)
        else:
            return 0
        

    def count_Mods(self):
        self.cursor = self.con.cursor()  # Creating the cursor object
        sql = "SELECT COUNT(*) FROM moderators"
        self.cursor.execute(sql)          # Execute the query
        result = self.cursor.fetchone()  # fetch one tuple
        self.cursor.close()              # Close the cursor
        if result:
            return result[0]             # return count value (first element)
        else:
            return 0

#UPDATE USER_____________________________________________________________________________________________________________________________
    def get_id(self,id):
        self.cursor = self.con.cursor()
        sql = "SELECT * FROM users WHERE u_id = %s"
        var = (id)
        self.cursor.execute(sql,var)
        # Printing the results
        try:
            self.con.commit()
            self.status = True
            print(self.status)
            self.data = self.cursor.fetchone()
            self.cursor.close()
            return self.status, self.data 
        except:
            self.con.rollback()
            self.status=False
            print(self.status)
            self.cursor.close()
            return self.status,[]
    
    def updates_user_data(self, ids, username, Email, password):
        print(type(ids))
        self.cursor = self.con.cursor()
        sql = "UPDATE users SET username = %s, email = %s, password = %s WHERE u_id = %s"
        var = (username, Email, password, ids)
        try:
            self.cursor.execute(sql, var)
            self.con.commit()
            self.status = True
            print("************************")
            print("Data Updated")
            return self.status
        except Exception as e:
            self.con.rollback()
            self.status = False
            print("************************")
            print("Data not Updated:", e)
            return self.status
        
    def get_Blog_id(self,id):
        self.cursor = self.con.cursor()
        sql = "SELECT * FROM blogs WHERE id = %s"
        var = (id)
        self.cursor.execute(sql,var)
        # Printing the results
        try:
            self.con.commit()
            self.status = True
            print(self.status)
            self.data = self.cursor.fetchone()
            self.cursor.close()
            return self.status, self.data 
        except:
            self.con.rollback()
            self.status=False
            print(self.status)
            self.cursor.close()
            return self.status,[]
        
    def updates_blog_data(self, ids, caption, description):
        print(type(ids))
        self.cursor = self.con.cursor()
        sql = "UPDATE blogs SET caption = %s, description = %s WHERE id = %s"
        var = (caption, description, ids)
        try:
            self.cursor.execute(sql, var)
            self.con.commit()
            self.status = True
            print("************************")
            print("Data Updated")
            return self.status
        except Exception as e:
            self.con.rollback()
            self.status = False
            print("************************")
            print("Data not Updated:", e)
            return self.status
        
    def get_Mod_id(self,id):
        self.cursor = self.con.cursor()
        sql = "SELECT * FROM moderators WHERE id = %s"
        var = (id)
        self.cursor.execute(sql,var)
        # Printing the results
        try:
            self.con.commit()
            self.status = True
            print(self.status)
            self.data = self.cursor.fetchone()
            self.cursor.close()
            return self.status, self.data 
        except:
            self.con.rollback()
            self.status=False
            print(self.status)
            self.cursor.close()
            return self.status,[]
        
    def update_Mod_data(self, ids, name,email, phone, password):
        print(type(ids))
        self.cursor = self.con.cursor()
        sql = "UPDATE moderators SET name = %s, email = %s,phone = %s,password = %s WHERE id = %s"
        var = (name,email, phone, password, ids)
        try:
            self.cursor.execute(sql, var)
            self.con.commit()
            self.status = True
            print("************************")
            print("Data Updated")
            return self.status
        except Exception as e:
            self.con.rollback()
            self.status = False
            print("************************")
            print("Data not Updated:", e)
            return self.status
#UPDATE PAGE DATA______________________________________________________________________________________________________________________________
    

    def get_page_id(self,id):
        self.cursor = self.con.cursor()
        sql = "SELECT * FROM users WHERE id = %s"
        var = (id)
        self.cursor.execute(sql,var)
        # Printing the results
        try:
            self.con.commit()
            self.status = True
            print(self.status)
            self.data = self.cursor.fetchone()
            self.cursor.close()
            return self.status, self.data 
        except:
            self.con.rollback()
            self.status=False
            print(self.status)
            self.cursor.close()
            return self.status,[]
    
    def updates_page_data(self, ids, name, Email, phone, add):
        print(type(ids))
        self.cursor = self.con.cursor()
        sql = "UPDATE users SET name = %s, email = %s, phone_number = %s,address = %s WHERE id = %s"
        var = (name, Email, phone, add)
        try:
            self.cursor.execute(sql, var)
            self.con.commit()
            self.status = True
            print("************************")
            print("Data Updated")
            return self.status
        except Exception as e:
            self.con.rollback()
            self.status = False
            print("************************")
            print("Data not Updated:", e)
            return self.status

    
    def delete_data(self,u_id):
        self.cursor = self.con.cursor()
        sql = "DELETE FROM users WHERE u_id = %s"
        var = (u_id)
        print(type(u_id))
        self.cursor.execute(sql,var)
        try:
            self.con.commit()
            self.status = True
            print("Data Deleted")
            return self.status
        except:
            self.con.rollback()
            self.status = False
            print("Data not Deleted")
            return self.status
        
    
    def delete_BLog(self,id):
        self.cursor = self.con.cursor()
        sql = "DELETE FROM blogs WHERE id = %s"
        var = (id)
        print(type(id))
        self.cursor.execute(sql,var)
        try:
            self.con.commit()
            self.status = True
            print("Data Deleted")
            return self.status
        except:
            self.con.rollback()
            self.status = False
            print("Data not Deleted")
            return self.status
        
        
    def delete_Mod(self,id):
        self.cursor = self.con.cursor()
        sql = "DELETE FROM moderators WHERE id = %s"
        var = (id)
        print(type(id))
        self.cursor.execute(sql,var)
        try:
            self.con.commit()
            self.status = True
            print("Data Deleted")
            return self.status
        except:
            self.con.rollback()
            self.status = False
            print("Data not Deleted")
            return self.status
# ********************************************************Like Dislike********************************************************************88

    # def likes(self ,id):
    #     self.cursor = self.con.cursor()
    #     sql = "SELECT * FROM blogs WHERE id = %s "
    #     var = (id)
    #     self.cursor.execute(sql,var)
    #     self.results = self.cursor.fetchone()
    #     if self.cursor.rowcount == 1:
    #         status = True
    #         print(status)
    #         self.cursor.close()
    #         return status   
    #     else:
    #         status = False
    #         print(status)
    #         self.cursor.close()
    #         return status

    def likes(self ,id):
        self.cursor = self.con.cursor()
        sql = "SELECT * FROM blogs WHERE id = %s "
        var = (id,)  # Make sure 'id' is in a tuple for the execute method
        self.cursor.execute(sql, var)
        self.results = self.cursor.fetchone()

        if self.results:
            print(f"Data found for blog ID {id}: {self.results}")
            num = self.results[7]
            print("total likes is:-------> ",num)
            num+=1
            print(num)
            sql1 = "UPDATE blogs SET likes = %s WHERE id = %s"
            var1 = (num, id)
            try:
                self.cursor.execute(sql1, var1)
                self.con.commit()
                self.status = True
                print("************************")
                print("Data Updated")
                # return self.status
            except Exception as e:
                self.con.rollback()
                self.status = False
                print("************************")
                print("Data not Updated:", e)
                # return self.status
                # You can now work with the data in self.results
        else:
            print(f"No data found for blog ID {id}.")
    def dis_like(self ,id):
        self.cursor = self.con.cursor()
        sql = "SELECT * FROM blogs WHERE id = %s "
        var = (id,)  # Make sure 'id' is in a tuple for the execute method
        self.cursor.execute(sql, var)
        self.results = self.cursor.fetchone()

        if self.results:
            print(f"Data found for blog ID {id}: {self.results}")
            num = self.results[8]
            print("total likes is:-------> ",num)
            num+=1
            print(num)
            sql1 = "UPDATE blogs SET dislikes = %s WHERE id = %s"
            var1 = (num, id)
            try:
                self.cursor.execute(sql1, var1)
                self.con.commit()
                self.status = True
                print("************************")
                print("Data Updated")
                # return self.status
            except Exception as e:
                self.con.rollback()
                self.status = False
                print("************************")
                print("Data not Updated:", e)
                # return self.status
                # You can now work with the data in self.results
        else:
            print(f"No data found for blog ID {id}.")
    
    def comm(self,comment_id, name_text, comment_text):
        self.cursor = self.con.cursor()
        # a1=0
        # a='active'
        sql = "INSERT INTO comments (name, comment, b_id) VALUES (%s,%s,%s);"
        var = ( name_text, comment_text, comment_id)
        self.cursor.execute(sql,var)

        try:
            self.con.commit()
            self.status = True
            self.cursor.close()
            return self.status
        except:
            self.con.rollback()
            self.status=False
            self.cursor.close()
            return self.status
        # pass