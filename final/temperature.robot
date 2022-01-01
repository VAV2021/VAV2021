*** Settings ***
Library        SeleniumLibrary

*** Variables ***
${browser}     chrome
${base_url}    https://www.unitconverters.net

*** Test Cases ***
Verify title
    Open Converter Home Page
    Title should be    Unit Converter

Temperature Conversion Test
    Temperature 77 Fahrenheit Should Be 25 Celsius
    Temperature 40 Celsius Should Be 104 Fahrenheit
    Temperature 0 Celsius Should Be 273.15 Kelvin
    Close browser

*** Keywords ***
Open Converter Home Page
    Open browser    ${base_url}    ${browser}

${unit} ${fromVal} ${calFrom} Should Be ${toVal} ${calTo}
    Click link    ${unit}
    Clear element text    name:fromVal
    Select from list by label    name:calFrom    ${calFrom}
    Select from list by label    name:calTo      ${calTo}
    Input text    name:fromVal   ${fromVal}
    Textfield value should be    name:fromVal    ${fromVal}
    Textfield value should be    name:toVal      ${toVal}
    ${actualVal}    Get value    name:toVal
    Log               ${fromVal} ${calFrom} equals ${actualVal} ${calTo}
    Log to Console    ${fromVal} ${calFrom} equals ${actualVal} ${calTo}
    Sleep             1
