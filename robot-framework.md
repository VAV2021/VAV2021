## Robot Framework

[Robot Framework](https://robotframework.org) is an
"automation framework" for testing and robotic process automation (RPA).
It uses an extensible English-like grammar.

[Getting Started](https://robotframework.org/#getting-started) - how to install
it, example, and links to some tutorials.

[QuickStart](https://github.com/robotframework/QuickStartGuide/blob/master/QuickStart.rst) the syntax with examples and some Python code (on Github). I didn't find it very useful.

[User Guide](http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html) is more useful.

[Standard Libraries](http://robotframework.org/robotframework/#standard-libraries) links to the Keyword reference for each of the standard libraries. Useful for constructing tests.


### Robot Framework Standard Libraries

[Standard Libraries](http://robotframework.org/robotframework/#standard-libraries) (see this page for links to each) included with robot framework are:

- [BuiltIn][] provides standard RF "keywords" like "should equal", logs
- [Collections][] provides keywords for using Python lists, collections, and dictionaries, such as "append to ..." or "get from dictionary", "list should contain ...".
- [DateTime][] keywords for getting date/time and testing date/times
- [Dialogs][] keywords for interacting with the user
- [OperatingSystem][] keywords for using operating system commands such as "run" to run a command, create and remove files and directories, check file existences or check a file contains a value
- [Process][] keywords for running processes; "run process", "start process" (run in background), wait for, stop processes
- Remote is part of the [remote library interface][remote-library]
- [Screenshot][] keywords to take a screenshot of application
- [String][] keywords for string manipulation, including regular expressions, split string into lines, verifying string contents
- [Telnet][] keywords for a connection over telnet (really? Telnet is insecure and deprecated. Probably uses SSH)
- [XML][] keywords for working with XML files or XML data

[BuiltIn]: http://robotframework.org/robotframework/latest/libraries/BuiltIn.html
[Collections]: http://robotframework.org/robotframework/latest/libraries/Collections.html
[DateTime]: http://robotframework.org/robotframework/latest/libraries/DateTime.html
[Dialogs]: http://robotframework.org/robotframework/latest/libraries/Dialogs.html
[OperatingSystem]: http://robotframework.org/robotframework/latest/libraries/OperatingSystem.html
[Process]: http://robotframework.org/robotframework/latest/libraries/Process.html
[Screenshot]: http://robotframework.org/robotframework/latest/libraries/Screenshot.html
[String]: http://robotframework.org/robotframework/latest/libraries/String.html
[Telnet]: http://robotframework.org/robotframework/latest/libraries/Telnet.html
[XML]: http://robotframework.org/robotframework/latest/libraries/XML.html
[remote-library]: https://github.com/robotframework/RemoteInterface

These libraries mostly provide an interface between RF's keyword language and Python libraries.

Other libraries (you have to install them yourself):

- [Browser Library][browser-library] control a web browser, test elements on a page, click elements,

- [SeleniumLibrary][selenium-library] another browser control library, using Selenium. 

- [Browser](https://marketsquare.github.io/robotframework-browser/Browser.html) Keywords reference with explanation


### RF Standard Tools

- Testdoc
- Tidy
- Libdoc
- Robot

### Test Cases

Generally 3 broad categories of tests in RF:

- Workflow tests
- High Level tests
- Data-Driven tests

### Writing Tests in Robot Framework

An RF file has extension `.robot` (by convention) and is divided into sections.
The sections begin with asterisk `*` but typically people write 3 asterisks:
```
*** Settings ***
Documentation     Play around with selenium library
...               more documentation
Library           SeleniumLibrary

*** Variables ***
${SITE_URL}    https://vaccine-haven.covid.com
${BROWSER}     Firefox

*** Keywords ***
# user defined expressions and actions

Open Application
    Open Browser  ${SITE_URL}  ${BROWSER}

*** Test Cases ***
Navigate to Home Page
    Open Application
    Title Should Be    Vaccine Haven
    Page Should Contain  Registration
```

In the above example, `Open Browser`, `Title Should Be`, `Page Should Contain` are RF **keywords** defined either in SeleniumLibrary or one of the built-in libraries.

**Spacing Before & Between Arguments** you must leave **at least 2 spaces** or **tab** before arguments (after a keyword phrase) and between arguments.


### Selenium Library

Installation:  `pip3 install robotframework-seleniumlibrary`.

Documentation:
- SeleniumLibrary <https://robotframework.org/SeleniumLibrary/> complete introduction
- [SeleniumLibrary Keywords](https://robotframework.org/SeleniumLibrary/SeleniumLibrary.html) single page reference (like Javadoc)
- 

Use in tests:

```robot
*** Settings ***
Documentation   Some test using seleniumlibrary
Libary          SeleniumLibrary

*** Variables ***
# variable names can contain spaces
${LOGIN URL}    https://localhost:8000/accounts/login/
${BROWSER}      Firefox
@{LISTVAR}      first   second   third   fourth
&{DICTVAR}      username=harry   password=hacker  email=harry@hackerone.com

*** Test Cases ***
Valid Login
	Open Browser to Login Page
	Input Username   demouser
	Input Password   demopass
	Submit

*** Keywords ***
# User-defined keywords (actions & expressions)

Open Browser to Login Page
    Comment this is a comment that is included in the output
	Open Browser  ${LOGIN URL}  ${BROWSER}

Input Username
	[Arguments]  ${username}
	Input Text	 usernamefield  ${username}

Input Password
	[Arguments]  ${password}
	Input Text	 passwordfield  ${password}

Submit
	Click Button login_button

*** Tasks ***
# User defined tasks

```

Complete example of login test using SeleniumLibrary:
<https://www.edureka.co/blog/robot-framework-tutorial/>.
(This is actually copied from other sources.)


[browser-library]: https://robotframework-browser.org/
[selenium-library]: https://robotframework.org/SeleniumLibrary/SeleniumLibrary.html

"Basic Concepts of Robot Framework" with focus toward RPA.
https://robocorp.com/docs/languages-and-frameworks/robot-framework/basics

