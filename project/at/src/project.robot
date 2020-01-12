*** Settings ***
Resource    ../resource/its.resource

*** Variables ***
${delete_success_message}    Project deleted successfully.
${add_member_success_message}    Add member successfully.

${test_account}    arron1234
${test_password}    arron_password
${test_name}    Arron
${test_member_account}    sam12345
${test_member_password}    sam_password
${test_member_name}    Sam
${test_project}    se

*** Test Cases ***
User Create New Project
    [Setup]   Create Test Account
    Open Login Page
    Go To Project List Page    ${test_account}    ${test_password}
    Create New Project    ${test_project}
    Wait Until Element Is Visible    xpath=//label[normalize-space()="${test_project}"]
    Location Should Be    ${backend_host}/${test_account}/${test_project}
    Close Browser And Delay    2
    [Teardown]   Delete Test Account And Project


Project Owner Delete Project
    [Setup]    Create Test Project And Account
    Open Login Page
    Go To Project Page    ${test_account}    ${test_password}    ${test_project}
    Wait Until Element Is Visible    xpath=//button[normalize-space()="刪除專案"]
    Click Button    xpath=//button[normalize-space()="刪除專案"]
    Alert Should Be Present    ${delete_success_message}
    Close Browser And Delay    2

Project Member Edit Project's Description
    [Setup]    Create Test Project And Account
    Open Login Page
    Go To Project Page    ${test_account}    ${test_password}    ${test_project}
    Edit Project description    This is se!
    Wait Until Element Is Visible    xpath=//p[normalize-space()="This is se!"]
    Close Browser And Delay    2
    [Teardown]   Delete Test Account And Project

Project Owner Add Project's Members
    [Setup]    Create Test Project And Account
    Open Login Page
    Go To Project Page    ${test_account}    ${test_password}    ${test_project}
    Click Button    xpath=//button[normalize-space()="Members"]
    Wait Until Element Is Visible    xpath=//button[normalize-space()="Add Member"]
    Click Button    xpath=//button[normalize-space()="Add Member"]
    Wait Until Element Is Visible    xpath=//input[@name="new_member_name"]
    Input Text    xpath=//input[@name="new_member_name"]    ${test_member_account}
    Click Button    xpath=//button[normalize-space()="Add"]
    Wait Until Element Is Visible    xpath=//td[normalize-space()="${test_member_name}"]
    Close Browser And Delay    2
    [Teardown]    Delete Test Account And Project

Project Owner Delete Project's Members
    [Setup]    Create Test Project And Account And Add Member To Project
    Open Login Page
    Go To Member Page    ${test_account}    ${test_password}   ${test_project}
    Click Remove Button    0
    Element Should Not Be Visible    xpath=//td[normalize-space()="${test_member_account}"]
    Close Browser And Delay    2
    [Teardown]    Delete Test Account And Project

Project Owner Edit Project Member's Role
    [Setup]    Create Test Project And Account And Add Member To Project
    Open Login Page
    Go To Member Page    ${test_account}    ${test_password}    ${test_project}
    Click Role    0    tester
    Close Browser And Delay    2
    [Teardown]    Delete Test Account And Project


***Keywords***
Create New Project
    [Arguments]    ${project_name}
    Click Button    xpath=//button[normalize-space()="新增專案"]
    Wait Until Element Is Visible    xpath=//input[@name="new_project_name"]
    Input Text    xpath=//input[@name="new_project_name"]    ${project_name}
    Click Button    xpath=//button[normalize-space()="Save Changes"]

Edit Project description
    [Arguments]   ${description}
    Click Button    xpath=//button[normalize-space()="Edit"]
    Wait Until Element Is Visible    xpath=//button[normalize-space()="Save"]
    Input Text    xpath=//textarea[@name="comment"]    ${description}
    Click Button    xpath=//button[normalize-space()="Save"]
    Wait Until Element Is Visible    xpath=//button[normalize-space()="Edit"]

Click Remove Button
    [Arguments]    ${index}
    @{buttons}    Get Webelements    xpath=//button[normalize-space()="Remove"]
    Click Element    @{buttons}[${index}]

Click Role
    [Arguments]    ${index}   ${role}
    @{roles}    Get Webelements    xpath=//span[normalize-space()="${role}"]
    Click Element    @{roles}[${index}]

Create Test Account
    Mongo Create User  ${test_account}    ${test_password}    ${test_name}    arron@email    user    arron_line
    Mongo Create User    ${test_member_account}    ${test_member_password}    ${test_member_name}    sam@email    user    sam_line

Create Test Project And Account
    Create Test Account
    Mongo Create Project    ${test_account}    ${test_project}

Delete Test Account And Project
    Mongo Delete Project    ${test_account}    ${test_project}
    Mongo Delete User    ${test_account}
    Mongo Delete User    ${test_member_account}

Create Test Project And Account And Add Member To Project
    Create Test Project And Account
    Mongo Add Project Member    ${test_account}    ${test_member_account}    ${test_project}
