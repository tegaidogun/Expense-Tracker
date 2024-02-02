<!DOCTYPE html>
<html>
<body>

<h1>Expense Tracker</h1>

<p>This Expense Tracker is a Flask-based web application that assists users in monitoring and managing their daily expenses in a simple and efficient manner.</p>

<h2>Features</h2>

<ul>
    <li><strong>User Authentication</strong>: Secure user registration and login to protect your expense data.</li>
    <li><strong>Add Expenses</strong>: Easily add new expenses with details like amount and description.</li>
    <li><strong>Edit Expenses</strong>: Modify existing expense entries effortlessly.</li>
    <li><strong>Delete Expenses</strong>: Remove unwanted expense entries from the list.</li>
    <li><strong>Monthly Overview</strong>: View your expenses grouped by months for better financial planning.</li>
    <li><strong>Responsive Design</strong>: A responsive design that works seamlessly on both desktop and mobile browsers.</li>
</ul>

<h2>Installation</h2>

<ol>
    <li><strong>Clone the Repository</strong>
        <pre><code>git clone https://github.com/tegaidogun/personal-expense-tracker.git</code></pre>
    </li>
    <li><strong>Setup Virtual Environment</strong>
        <pre><code>python3 -m venv venv
source venv/bin/activate  # On Windows use `.\venv\Scripts\activate`</code></pre>
    </li>
    <li><strong>Install Dependencies</strong>
        <pre><code>pip install -r requirements.txt</code></pre>
    </li>
    <li><strong>Initialize Database</strong>
        <pre><code>python database.py</code></pre>
    </li>
    <li><strong>Run the Application</strong>
        <pre><code>flask run</code></pre>
     <strong>Run the Application (Debug Mode)</strong>
        <pre><code>python app.py</code></pre>
    </li>
</ol>

<h2>Usage</h2>

<ol>
    <li>Register a new user account.</li>
    <li>Login with your credentials.</li>
    <li>Start adding, editing, or deleting your expenses.</li>
    <li>View your monthly expense overview on the home page.</li>
