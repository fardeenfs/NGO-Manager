# NGO Manager (Membership, Expense/Income Tracker, Dues Billing, Financial Reports)

<h3>Technologies Used</h3>
This is a ready-to-use web app built on Django/Python in the Backend and uses plain HTML5, CSS, Javascript, JQuery and Bootstrap in the frontend. Most of the backend functionality have been complete (refer to the 'Under Development' subsection to see what's left). The frontend is still under development and I am planning to shift to React. The database software used for this purpose is PostgreSQL. 

<h3>Project Brief</h3>
This is an app built primarily for NGO's. If you are a non-profit, you are welcome to use the code for your purposes. The project consists of 4 major functionalities:<br>
1) <b>Membership Management</b> : You can add/remove members and create families from existing members <br>
2) <b>Expense/Income Tracker</b>: You can add income and expense records, generate invoices for them, and even view annual reports. <br>
3) <b>Dues Billing </b>: The organisation may have a membership fee or multiple types of fees that are to be paid by all/some of the members. You can apply the fees to all the members, or    some of them using the filters available. Receipts shall be generated automatically for every transaction and is availble for print at any time. I have also added the flexibility of individually applying dues to members individually. To use this feature, ensure that all the members have been added to membership management feature.<br>
4) <b>Financial Reports</b>: You have option to customize reports for download at any time during an year.
<br><br>
Depending on your organization needs, you may not need all the functionalities or need more functionalities. The project has been build with that in mind. You can use it for just tracking income/expense, or just managing memebers. The project should work error free when some of these features are used on its own.
<br>
<h3>Project Usage And Set Up</h3>
<ol> 
 <li> Clone the repository to your local machine.</li>
 <li> Install a database software of your choice. For this project, I have used PostgreSQL. I would recommend you to do the same as I haven't tested it with other DBMS like MySQL yet, but I believe it should work nevertheless. Once you have finished setting up the database software on your machine, create a new database and configure the settings.py file under the folder 'NGO Manager' with the local database variables. The way to do this is similar to how you would set up the database for any Django project. You can views the steps at: https://docs.djangoproject.com/en/3.2/ref/databases/
 <li> Open the terminal, navigate to the directory. Run the command "python3 manage.py makemigrations" and then "python3 manage.py migrate". If the database has been configured properly, all the required tables will now be automatically created in the database.</li>
 <li> Create a superuser for the Django project with the command "python3 manage.py createsuperuser"</li>
 <li> Once the superuser has been created, start the local server with the command "python3 manage.py runserver"</li>
 <li> Now you will be redirected to a login screen, login with the credentials with the superuser account you just created.</li>
 <li> That's almost it. The membership management feature should now work (Refer to the 'Usage' subsection before you do). The Income/Expense Trackers and Billing won't work just yet, as we will need to set up the accounts for it to work. If you attempt to use any of these features, you will most likely get an error.</li>
 <li>Head over to the 'Accounts' tab. Click on add new account. Enter the Bank Name, Account Type, Account Number (optional, for your reference. Type 999 to skip),and your current account balance. Click on 'Submit'. Your account is now saved. Repeat the process for all the accounts. The Dues Billing and Income/Expense Tracker needs at least one account to be created.</li>
 <li> Now the dues billing and income/expense trackers should work!</li>
 
 


