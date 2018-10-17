*** Settings ***
Library  BuiltIn

*** Test Cases ***

Test 1
    [Tags]  cant_run_on_rig_1
    Log     Test 1 Yeah
    Sleep	${delay}
    Log		${print}

Test 2
    [Tags]  cant_run_on_rig_1  cant_run_on_rig_2
    Log     Test 2 Yeah
    Sleep	${delay}
    Log		${print}

Test 3
    [Tags]  cant_run_on_rig_1
    Log     Test 1 Yeah
    Sleep	${delay}
    Log		${print}

Test 4
    [Tags]  cant_run_on_rig_1
    Log     Test 2 Yeah
    Sleep	${delay}
    Log		${print}

Test 5
    [Tags]  cant_run_on_rig_1
    Log     Test 1 Yeah
    Sleep	${delay}
    Log		${print}

Test 6
    [Tags]  test2_tag
    Log     Test 2 Yeah
    Sleep	${delay}
    Log		${print}

Test 7
    [Tags]  test1_tag
    Log     Test 1 Yeah
    Sleep	${delay}
    Log		${print}

Test 8
    [Tags]  test2_tag
    Log     Test 2 Yeah
    Sleep	${delay}
    Log		${print}
