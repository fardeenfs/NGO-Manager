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
Depending on your organization needs, you may not need all the functionalities or need more functionalities. The project has been build with that in mind. You can use it for just tracking income/expense, or just managing memebers. The project should work error free when these features are used on its own.
<br>
<h3>Project Usage And Set Up</h3>
<ol> 
 <li> Clone the repository to your local machine.</li>
 <li> Install a database software of your choice. For this project, I have used PostgreSQL. I would recommend you to do the same as I haven't tested it with other DBMS like MySQL yet, but I believe it should work nevertheless. Once you have finished setting up the database software on your machine, create a new database and configure the settings.py file under the folder 'NGO Manager' with the local database variables. The way to do this is similar to how you would set up the database for any Django project. You can views the steps at: https://docs.djangoproject.com/en/3.2/ref/databases/
 <li> Open the terminal, navigate to the directory. Run the command "python manage.py makemigrations" and then "python manage.py migrate". If the database has been configured properly, all the required tables will now be automatically created in the database.</li>
 <li> Run the following SQL command "insert into sitewide values(1,'FY21','2021-2022','2021-01-01','2021-12-31','2021 Year Records')". These values can be replaced depending on the year you are working in. I am working on a programmatic fix to skip this step.</li>
 <li> Create a superuser for the Django project with the command "python manage.py createsuperuser"</li>
 <li> Once the superuser has been created, start the local server with the command "python manage.py runserver"</li>
 <li> Now you will be redirected to a login screen, login with the credentials with the superuser account you just created.</li>
 <li> That's almost it. The membership management feature should now work (Refer to the 'Usage' subsection before you do). The Income/Expense Trackers and Billing won't work just yet, as we will need to set up the accounts for it to work. If you attempt to use any of these features, you will most likely get an error.</li>
 <li>Head over to the 'Accounts' tab. Click on add new account. Enter the Bank Name, Account Type, Account Number (optional, for your reference. Type 999 to skip),and your current account balance. Click on 'Submit'. Your account is now saved. Repeat the process for all the accounts. The Dues Billing and Income/Expense Tracker needs at least one account to be created.</li>
 <li> Now the dues billing and income/expense trackers should work! (READ USAGE INSTRUCTIONS BEFORE YOU START)</li>
 </ol>
 
 <h3> Usage</h3>
 <h4> Part 1: Membership Management</h4>
 <ol>
  <li>All members that are added SHOULD BE attached to a family. If there is a new member of a new family to be added, the 'ADD FAMILY' option should be used to add the member and instantiate a new family for the member. The 'ADD MEMBER' option SHOULD NOT BE used to create the first member of the family (This will definitely return an error). Any subsequent members to an existing family should be added using the 'ADD MEMBER' option. </li>
  <li>All families need to have one and only one HEAD. Usually the member added first using the 'ADD FAMILY' option is considered the head of the family. If this is to be changed due to <i>death</i>, <i>divorce</i> or <i>any other circumstance</i>, ENSURE that another member(new head) of the family is made the HEAD (search the member using there member number in the home page, and choose 'edit', check the head option). The former head has to then be edited and the head option is to be unchecked .  Not having a head for a family may lead to errors, this instance has not been tested. </li> 
  <li>In the event of the death of a family member, edit the member and uncheck 'Is Alive?' and 'Is Active?'. Once this is done, the pending dues of the inactive member is passed on to the head of the family. If the deceased, family member is the head of the family, ensure that STEP 2 is followed before following STEP 3.</li>
  </ol>
 <h4> Part 2: Income Expense Tracking</h4>
 <ol>
  <li>This option can be used for transactions like one-time donations (income), utility costs(expense) and wages(expenses).</li>
  <li>First, create the record classes, using the "Add Record Class" button. A record class is a classification of income/expense. For example, you may want to categorize all the incoming donations together. So the name of the Record Class can be "Donations" and the type will be "Income". For the 'Class Account' choose the account which is to be used to collect the donations. You should see all the accounts that have been added as a dropdown, so choose one. Once its submitted, you should now be able to see the option "Donations" under the "Select Income Type" option of the "Add Income Record". Repeat the process as needed. You might want to create a separate record class for expenses like utility bills and other sources of income like assets.</li>
  <li>You can now create Income And Expense Records as needed. If you make a mistake, you can choose the cancel option for the corresponding record to remove it.</li>
  <li>The 'Remarks' button will show you an alert, with the remarks that was entered during record creation.</li>
  <li>The 'Print' option will return you to a printable invoice page, if it is needed for record-keeping or other administrative purposes. </li>
 </ol>
  <h4> Part 3: Dues Billing</h4>
 <ol>
  <li> Due types need to be created first. Head over to the Dues Settings page. Click on 'New Due Type'. 'Due ID' is for your reference. Make sure its unique so that you can differentiate later on. 'Due Type' is the name/type of due. For instance, the due can be a "Membership Fee" all members have to pay. In this case 'Due Type' will be "Membership Fee". 'Due Fine Amount' is the fine a member has to pay on top of the due, if the amount is not paid in full by the end of the year.</li>
  <li> For the fields from 'Is Head?' to 'Is Male?' the following format applies
   <ul>
    <li> '-1' stands for Do Not Use Filter (If -1 is used for 'Is Male?', the fact that a person is male or female is not considered to apply the due.)</li>
    <li> '0' stands for False cases (If 0 is used for 'Is Male?', the due is applied only if a person is NOT Male)</li>
    <li> '1' stand for True cases (If 1 is used for 'Is Male?', the due is applied only if a person is Male)</li>
   </ul>
   So if a due is to be applied to everyone who is Male and Employed, 'Is Male' will be '1' and 'Is Employed' will be '1'. Since we do not want to use the other filters, all other options will be '-1'.</li>
 <li>Choose the Account Serial of the account where the income from this Due Type will go to. And that's it, you have created the first due.</li>
 <li>Now that the Due is created, click on 'Apply All'. This will apply the 'Due' to all the members based on the filters chosen earlier. You can verify if the due has been applied by searching up the outstanding amount of some of the fmailies. For flexibility reasons, if the due has to be applied to a few other people not in the filter, you can type in the Member No. to the 'Apply To Member' field and click 'Apply'. This will apply the due to that particular member too.</li>
 <li> If for some reason you want to undo the 'Apply All', you can click on the 'Override' button. This will remove that particular due for everyone.
 <li>When a member pays, head over to 'Home', search the member's family number and then click on 'View All Details'. This will show you the break up of the dues, member-wise. Type in the amount paid in the pay area respective to the member name and due type paid for. Payment can be made for multiple dues and members in the family at the same time. Verify the total amount next to the 'Pay' button at the end. You should now see that the Balance will be reduced. Head over to the receipt tab in the top. You will see that a new receipt will be created. You can print and also cancel it, if the payment as done accidentally. When the receipt is cancelled, the due amount balance will also revert back to before the payment was done.</li>
 <li> If you want to cancel or offer a discount to a particular member for a particular due type, type in the amount in the pay area to be cancelled/discounted. Click on 'Override'. This will reduce the balance to be paid.</li>
 <li> Sometimes, for smaller amounts, it might be hectic to generate receipts for every member. In this scenario, the 'Mark As Paid' option in Dues Settings can be used to generate receipts and mark the due as paid for everyone. If a few people haven't paid, you can head over to their family and manually cancel their receipts.</li>
 </ol>
 
<h4> Part 4: Accounts</h4>
<ol>
 <li>You can view the balances of all the accounts here. All the due income, record incomes and expenses can be seen in the last column for every account. </li>
 <li>All due income, record incomes and expenses are added/deducted to the Cash in Hand. If money is deposited to the bank, use the 'Deposit/Withdraw' option. This should transfer that amount from the cash in hand column to the cash in bank column. The withdraw option can be used in the inverse scenario. If money is to be transfered between accounts use the 'Transfer' option.</li>
 <li>All such manual manipulations ('Deposit/Withdraw' and 'Transfer') to the account can be seen in the Transaction Records tab, with the time and user who performed it for security purposes.</li>
</ol>

<h3> Under Development</h3>
<ul>
 <li> UI Fixes. I have used basic UI themes and will be trying to switch to React in the upcoming commits </li>
 <li> Report Features like graphs to show income and expenses is being worked upon</li>
 <li> Looking to use API of third party payment providers like Stripe to allow members to do payments through the website </li>
 <li> Error Handling of the project needs improvement. I am looking at alternative system designs to make it more user friendly</li>
</ul>

DISCLAIMER: This project has been tested and some known bugs have been fixed. There could nevertheless be potential bugs in the code and by using this code you agree that I will not be held responsible for any losses incurred. All non-profits are welcome to use this project for free. If you are a profit-making business, kindly contact me at fardeenfaisal.fs@gmail.com before using the code.


All contributions and suggestions are welcome! Feel free to create a pull request and report bugs/issues.

