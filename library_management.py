#Build a simple command-line based library management system that allows users to manage books and members 
#using basic CRUD (Create, Read, Update, Delete) operations directly within the application.
import random

class LibraryManagement:

    def __init__(self,book,member):
        self.book=[]
        self.member=[]

    #function to add details to library database
    def add_books(self,id,title,author):
        self.book.append({"ID:":id,"title":title,"Author":author})
    
    #function to add details of a member
    def add_member(self,id,name):
        self.member.append({"ID":id,"Name":name})
    
    #function to read the details of the books
    def read_book(self):
        for book in self.book:
            print(f"ID : {book['ID']}, Title : {book['title']}, Author : {book['Author']}")
    
    #function to read details of memebers
    def read_members(self):
        for member in self.member:
            print(f"ID : {member['ID']} , Name : {member['Name']}")
    
    #function to Update the details of book
    def update_detail_b(self,id,title,author):
        for book in self.book:
            if book['ID'] == id:
                book['Title']=title
                book['Author']=author
                print("Updated the details")
            else:
                print("No such reocrd found")

    #function to update the details of member
    def update_detail_m(self,id,name):
        for member in self.member:
            if member['ID'] == id:
                member['Name'] = name
                print("Updated the details")
            else:
                print("No such record found")
    
    #function to delete the detail of the book
    def delete_book(self,id):
        for book in self.book:
            if book['ID'] == id:
                del book
                print("Successfully deleted the records")
            else:
                print("No such records exist")
    
    #function to delete the detail of the member
    def delete_member(self,id):
        for member in self.member:
            if member['ID'] == id:
                del member
                print("Successfully deleted the records")
            else:
                print("No such records exist")

library=LibraryManagement()
flag=True
while(flag):
    print('''
         1.ADD BOOK
         2.READ BOOK
         3.UPDATE BOOK
         4.DELETE BOOK
         5.ADD MEMBER
         6.READ MEMBER
         7.UPDATE MEMBER
         8.DELETE MEMBER''') 