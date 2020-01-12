*** Settings ***
Resource    ../resource/its.resource

*** Variables ***
${admin_username}    root
${admin_password}    root
${register_success_message}    Create account succeed
${edit_password_success_message}    Update password succeed
${test_account}    arron1234
${test_password}    arron_password

*** Test Cases ***

System Administrator Create General User Account
    Open Login Page
    User Login    ${admin_username}    ${admin_password}
    Wait Until Element Is Visible    xpath=//h2[normalize-space()="Profile"]
    Go To    ${backend_host}/${account_manage_url}
    Create New Account    ${test_account}    Arron    arron@email    ${test_password}    user
    Scroll Element Into View    xpath=//td[normalize-space()="Arron"]
    Wait Until Element Is Visible    xpath=//td[normalize-space()="Arron"]
    Close Browser And Delay    2
    [Teardown]    Delete Test Account

System Administrator Create Manager Account
    Open Login Page
    User Login    ${admin_username}    ${admin_password}
    Wait Until Element Is Visible    xpath=//h2[normalize-space()="Profile"]
    Go To    ${backend_host}/${account_manage_url}
    Create New Account    ${test_account}    Arron    arron@email    ${test_password}    manager
    Scroll Element Into View    xpath=//td[normalize-space()="Arron"]
    Wait Until Element Is Visible    xpath=//td[normalize-space()="Arron"]
    Close Browser And Delay    2
    [Teardown]    Delete Test Account

User Register New Account And Login By New Account
    Open Login Page
    Click Button  xpath=//button[normalize-space()="Sign Up"]
    Register Account    ${test_account}    arron    arron@email    ${test_password}
    Alert Should Be Present    ${register_success_message}
    Location Should Be    ${backend_host}/${sign_in_url}
    User Login    ${test_account}    ${test_password}
    Close Browser And Delay    2
    [Teardown]   Delete Test Account

User Edit Profile Data
    [Setup]    Create Test Account
    Open Login Page
    User Login    ${test_account}    ${test_password}
    Wait Until Element Is Visible    xpath=//button[normalize-space()="更新個人資料" ]
    Element Should Be Disabled    xpath=//button[normalize-space()="更新個人資料" ]
    Input Text    xpath=//input[@name="name"]    arron_new_name
    Input Text    xpath=//input[@name="email"]    arron@new.email
    Input Text    xpath=//input[@name="lineID"]    arron_new_line
    Element Should Be Enabled    xpath=//button[normalize-space()="更新個人資料" ]
    Click Button    xpath=//button[normalize-space()="更新個人資料" ]
    Element Should Be Disabled    xpath=//button[normalize-space()="更新個人資料" ]
    Close Browser And Delay    2
    [Teardown]    Delete Test Account


User Edit Password And Login By New Password
    [Setup]    Create Test Account
    Open Login Page
    User Login    ${test_account}    ${test_password}
    Wait Until Element Is Visible    xpath=//button[normalize-space()="修改密碼"]
    Edit Password    arron_password    arron_new_password
    Alert Should Be Present    ${edit_password_success_message}
    Sign Out
    User Login    ${test_account}    arron_new_password
    Wait Until Element Is Visible    xpath=//button[normalize-space()="修改密碼"]
    Close Browser And Delay    2
    [Teardown]    Delete Test Account

***Keywords***
Go TO Account Manage Page
    Go To    ${backend_host}/${account_manage_url}

Create New Account
    [Arguments]    ${username}    ${name}    ${email}    ${password}    ${role}
    Wait Until Element Is Visible    xpath=//button[normalize-space()="Create Account"]
    Click Button    xpath=//button[normalize-space()="Create Account"]
    Input Text    xpath=//input[@name="new_username"]    ${username}
    Input Text    xpath=//input[@name="new_name"]    ${name}
    Input Text    xpath=//input[@name="new_email"]    ${email}
    Input Text    xpath=//input[@name="new_password"]    ${password}
    Select From List By Label    xpath=//select[@name="new_role"]    ${role}
    Click Button    xpath=//button[normalize-space()="Register"]
    Wait Until Element Is Visible    xpath=//button[normalize-space()="Create Account"]

Register Account
    [Arguments]    ${username}    ${name}    ${email}    ${password}
    Wait Until Element Is Visible    xpath=//button[normalize-space()="Register"]
    Input Text    xpath=//input[@name="username"]    ${username}
    Input Text    xpath=//input[@name="name"]    ${name}
    Input Text    xpath=//input[@name="email"]    ${email}
    Input Text    xpath=//input[@name="password"]    ${password}
    Click Button    xpath=//button[normalize-space()="Register"]

Edit Password
    [Arguments]    ${old_password}    ${new_password}
    Click Button    xpath=//button[normalize-space()="修改密碼"]
    Wait Until Element Is Visible    xpath=//input[@name="oldPassword"]
    Wait Until Element Is Visible    xpath=//input[@name="newPassword"]
    Input Text    xpath=//input[@name="oldPassword"]    ${old_password}
    Input Text    xpath=//input[@name="newPassword"]    ${new_password}
    Click Button    xpath=//button[normalize-space()="Save Changes"]

Delete Test Account
    Mongo Delete User    ${test_account}

Create Test Account
    Mongo Create User    ${test_account}    ${test_password}    Arron    arron@email    arron_line
