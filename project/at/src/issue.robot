*** Settings ***
Resource    ../resource/its.resource

*** Variables ***
${test_account}    arron1234
${test_password}    arron_password
${test_name}    Arron
${test_member_account}    sam12345
${test_member_password}    sam_password
${test_member_name}    Sam
${test_project}    se
${test_issue_title}    first_issue
${test_issue_comment}    first_comment
${test_issue_number}    1
${test_comment}    first_issue_comment

*** Test Cases ***
Project Member Report An Issue
    [Setup]    Create Test Project And Account And Add Member To Project
    Open Login Page
    Go To Issue Page   ${test_account}    ${test_password}    ${test_project}
    Create Issue    ${test_issue_title}    ${test_issue_comment}
    Close Browser And Delay    2
    [Teardown]    Delete Test Account And Project

Project Manager Assign An Issue To Project Members
    [Setup]    Create Test Issue Data
    Open Login Page
    Go To Issue Page   ${test_account}    ${test_password}    ${test_project}
    Scroll Element Into View    xpath=//h5[normalize-space()="#${test_issue_number} ${test_issue_title}"]
    Click Element    xpath=//h5[normalize-space()="#${test_issue_number} ${test_issue_title}"]
    Wait Until Element Is Visible    xpath=//button[normalize-space()="Add Assignee"]
    Click Button    xpath=//button[normalize-space()="Add Assignee"]
    Wait Until Element Is Visible    xpath=//a[normalize-space()="${test_member_account}"]
    Click Element    xpath=//a[normalize-space()="${test_member_account}"]
    Wait Until Element Is Visible    xpath=//div[@class="NameList list-group-item"]
    Close Browser And Delay    2
    [Teardown]    Delete Test Account And Project

Project Manager Report An Issue And Assign To Project Members
    [Setup]    Create Test Project And Account And Add Member To Project
    Open Login Page
    Go To Issue Page   ${test_account}    ${test_password}    ${test_project}
    Create Issue And Assign    ${test_issue_title}    ${test_issue_comment}    ${test_member_account}
    Wait Until Element Is Visible    xpath=//div[@class="NameList list-group-item"]
    Close Browser And Delay    2
    [Teardown]    Delete Test Account And Project

Project Member Report A Comment
    [Setup]    Create Test Issue Data
    Open Login Page
    Go To Issue Page   ${test_account}    ${test_password}    ${test_project}
    Click Element    xpath=//h5[normalize-space()="#${test_issue_number} ${test_issue_title}"]
    Wait Until Element Is Visible    xpath=//textarea[@name="comment"]
    Input Text    xpath=//textarea[@name="comment"]    ${test_comment}
    Click Button    xpath=//button[normalize-space()="Submit Comment"]
    Wait Until Element Is Visible    xpath=//p[normalize-space()="${test_comment}"]
    Close Browser And Delay    2
    [Teardown]    Delete Test Account And Project

Project Member Change Issue's Attributes
    [Setup]    Create Test Issue Data
    Open Login Page
    Go To Issue Page   ${test_account}    ${test_password}    ${test_project}
    Click Element    xpath=//h5[normalize-space()="#${test_issue_number} ${test_issue_title}"]
    Wait Until Element Is Visible    xpath=//textarea[@name="comment"]
    Click Attributes    low    medium    no
    Wait Until Element Is Visible    xpath=//span[@class="level badge badge-success" and normalize-space()="low"]
    Wait Until Element Is Visible    xpath=//span[@class="level badge badge-warning" and normalize-space()="medium"]
    Wait Until Element Is Visible    xpath=//span[@class="level badge badge-danger" and normalize-space()="no"]
    Close Browser And Delay    2
    [Teardown]    Delete Test Account And Project

Project Member Change Issue's State
    [Setup]    Create Test Issue Data
    Open Login Page
    Go To Issue Page   ${test_account}    ${test_password}    ${test_project}
    Click Element    xpath=//h5[normalize-space()="#${test_issue_number} ${test_issue_title}"]
    Wait Until Element Is Visible    xpath=//textarea[@name="comment"]
    Click Button    xpath=//button[normalize-space()="Close Issue"]
    Wait Until Element Is Visible    xpath=//button[normalize-space()="Reopen Issue"]
    Close Browser And Delay    2
    [Teardown]    Delete Test Account And Project

Project Member Read Issue Statistical Report Of Project
    [Setup]    Create Test Assignee Data
    Open Login Page
    Go To Issue Page   ${test_account}    ${test_password}    ${test_project}
    Click Button    xpath=//button[normalize-space()="Issue Dashboard"]
    Wait Until Element Is Visible    xpath=//a[normalize-space()="${test_issue_title}"]
    Close Browser And Delay    2
    [Teardown]    Delete Test Account And Project

Project Member Select A Particular Member In The Issue Statistical Report Of Project
    [Setup]    Create Test Assignee Data
    Open Login Page
    Go To Issue Page   ${test_account}    ${test_password}    ${test_project}
    Click Button    xpath=//button[normalize-space()="Issue Dashboard"]
    Click Button    xpath=//button[normalize-space()="all"]
    Click Element    xpath=//a[normalize-space()="${test_member_account}"]
    Wait Until Element Is Visible    xpath=//a[normalize-space()="${test_issue_title}"]
    Close Browser And Delay    2
    [Teardown]    Delete Test Account And Project

***Keywords***
Create Issue
    [Arguments]    ${title}    ${comment}
    Click Button    xpath=//button[normalize-space()="New issue"]
    Wait Until Element Is Visible    xpath=//input[@name="title"]
    Wait Until Element Is Visible    xpath=//textarea[@name="comment"]
    Input Text    xpath=//input[@name="title"]    ${title}
    Input Text    xpath=//textarea[@name="comment"]    ${comment}
    Click Button    xpath=//button[normalize-space()="Submit new issue"]
    Wait Until Element Contains    xpath=//h2    ${title}

Create Issue And Assign
    [Arguments]    ${title}    ${comment}    ${member}
    Click Button    xpath=//button[normalize-space()="New issue"]
    Wait Until Element Is Visible    xpath=//input[@name="title"]
    Wait Until Element Is Visible    xpath=//textarea[@name="comment"]
    Input Text    xpath=//input[@name="title"]    ${title}
    Input Text    xpath=//textarea[@name="comment"]    ${comment}
    Wait Until Element Is Visible    xpath=//button[normalize-space()="Add Assignee"]
    Click Button    xpath=//button[normalize-space()="Add Assignee"]
    Wait Until Element Is Visible    xpath=//a[normalize-space()="${member}"]
    Click Element    xpath=//a[normalize-space()="${member}"]
    Click Button    xpath=//button[normalize-space()="Submit new issue"]
    Wait Until Element Contains    xpath=//h2    ${title}

Click Attributes
    [Arguments]    ${severity}    ${priority}    ${reproducible}
     @{level}    Get Webelements    xpath=//span[normalize-space()="${severity}"]
     Click Element    @{level}[0]
     @{level}    Get Webelements    xpath=//span[normalize-space()="${priority}"]
     Click Element    @{level}[1]
     Click Element    xpath=//span[normalize-space()="${reproducible}"]

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

Create Test Issue Data
    Create Test Project And Account And Add Member To Project
    Mongo Create Issue    ${test_account}    ${test_member_account}    ${test_project}    ${test_issue_title}    ${test_issue_comment}

Create Test Assignee Data
    Create Test Issue Data
    Mongo Add Assignees    ${test_issue_number}    ${test_member_account}
