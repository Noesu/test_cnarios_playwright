# Role-Based Login Flow

## Background

https://www.cnarios.com/challenges/login-flow#challenge

This challenge simulates a basic role-based authentication flow. Users can log in using dummy credentials displayed on
the login page. Depending on their role, the system displays a different dashboard (Admin or User).

#### Objectives:

- Validate login form input fields
- Verify error message on invalid credentials
- Login as user and validate user dashboard
- Login as admin and validate admin dashboard
- Verify logout functionality resets the session

#### Requirements:

- Create a login form with username and password fields
- Validate that empty fields show an error
- Show error message on invalid credentials
- Render user dashboard after login with User credentials
- Render admin dashboard after login with Admin credentials
- Implement logout that resets the state and returns to login page

#### Acceptance Criteria:

- Login form should validate empty fields and incorrect inputs
- Admin should see Admin Dashboard after login
- User should see User Dashboard after login
- Logout should clear session and return to login form
- Dummy credentials should be visible on login screen for practice

#### Hints:

- Locate input fields and buttons using labels or roles instead of CSS classes
- Automate both negative cases (empty/invalid credentials) and positive cases (valid user/admin login)
- Verify role-based dashboards by checking text like 'Admin Dashboard' or 'User Dashboard'
- Ensure error messages and alerts are visible when validation fails
- After logout, confirm that the login form is displayed again with fields reset

## Test-cases

#### LF_001	Empty fields validation	Error message 'Both fields are required.' is shown

Attempt login with empty username and password!

Steps to Execute:
1. Navigate to login page
2. Leave username and password empty
3. Click on login button
4. Verify error message is displayed

---

#### LF_002	Invalid credentials	Error message 'Invalid username or password.' is shown

Enter invalid username/password combination

1. Navigate to login page
2. Enter username 'wrongUser' and password 'wrongPass'
3. Click on login button
4. Verify error message is displayed

---

#### LF_003	Login as User	User dashboard is displayed with welcome message and User role info

Login with valid User credentials and verify User dashboard

1. Navigate to login page
2. Enter username 'user' and password 'user123'
3. Click on login button
4. Verify welcome message for 'user'
5. Verify User dashboard content is shown

---

#### LF_004	Login as Admin	Admin dashboard is displayed with welcome message and Admin role info

Login with valid Admin credentials and verify Admin dashboard

1. Navigate to login page
2. Enter username 'admin' and password 'admin123'
3. Click on login button
4. Verify welcome message for 'admin'
5. Verify Admin dashboard content is shown

---

#### LF_005	Logout functionality	Session is cleared and login form is displayed again

Logout from User/Admin dashboard and verify return to login form

1. Login with valid credentials
2. Click on logout button
3. Verify login form is displayed
4. Verify fields are reset to empty