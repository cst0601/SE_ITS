*** Settings ***
Library    Selenium2Library
Library    ../lib/UserManager.py
Library    ../lib/ProjectManager.py

*** Variables ***
${browser}    chrome
${backend_host}    http://127.0.0.1:5000
${account_manage_url}    accountmanage
${sign_in_url}    sign_in

*** Keywords ***
Close Browser And Delay
    [Arguments]    ${timeout}
    Sleep    ${timeout}
    Close Browser

Open Login Page
    Open Browser    ${backend_host}/sign_in    ${browser}
    Wait Until Element Is Visible    xpath=//nav

User Login
    [Arguments]    ${username}    ${password}
    Wait Until Element Is Visible    xpath=//input[@name="username"]
    Wait Until Element Is Visible    xpath=//input[@name="password"]
    Input Text    xpath=//input[@name="username"]    ${username}
    Input Text    xpath=//input[@name="password"]    ${password}
    Click Button    xpath=//button[normalize-space()="Login"]

Sign Out
    Run Keyword And Ignore Error    Click Element    xpath=//button[@class="navbar-toggler collapsed"]
    Run Keyword And Ignore Error    Wait Until Element Is Visible    xpath=//a[normalize-space()="Sign out"]
    Click Element    xpath=//a[normalize-space()="Sign out"]

Go To Project List Page
    [Arguments]    ${username}    ${password}
    User Login    ${username}    ${password}
    Wait Until Element Is Visible    xpath=//button[normalize-space()="我的專案"]
    Click Button    xpath=//button[normalize-space()="我的專案"]
    Wait Until Element Is Visible    xpath=//button[normalize-space()="新增專案"]
    Location Should Be    ${backend_host}/${username}/projects

Go To Member Page
    [Arguments]    ${username}    ${password}    ${project}
    Go To Project Page    ${username}    ${password}    ${project}
    Click Button    xpath=//button[normalize-space()="Members"]
    Wait Until Element Is Visible    xpath=//h2[normalize-space()="Project Member"]

Go To Project Page
    [Arguments]    ${username}    ${password}    ${project}
    Go To ProjectList Page    ${username}    ${password}
    Scroll Element Into View    xpath=//h4[normalize-space()="${project}"]
    Click Element    xpath=//h4[normalize-space()="${project}"]
    Wait Until Element Is Visible    xpath=//label[normalize-space()="${project}"]

Go TO Issue Page
    [Arguments]    ${username}    ${password}    ${project}
    Go To Project Page    ${username}    ${password}    ${project}
    Wait Until Element Is Visible    xpath=//button[normalize-space()="Issues"]
    Click Button    xpath=//button[normalize-space()="Issues"]
    Wait Until Element Is Visible    xpath=//button[normalize-space()="New issue"]
