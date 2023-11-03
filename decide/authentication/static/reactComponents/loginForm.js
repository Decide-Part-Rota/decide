"use strict";

const createLoginForm = React.createElement;

class LoginForm extends React.Component {
  render() {
    return createLoginForm(
        "body",
        {},
        createLoginForm("table",
            {className:"table"},
            createLoginForm(
                "tr",{},
                createLoginForm("th",{scope:"row"},"Username / Email"),
                createLoginForm(
                    "td",{},
                    createLoginForm("input",{type:"text",name:"username"}),
                )
            ),
            createLoginForm("tr",{},
                createLoginForm("th",{scope:"row"},"Password"),
                createLoginForm("td",{},
                    createLoginForm("input",{type:"password",name:"password"}),
                ),
            ),
        ),
    );}
    
}

const domContainerLoginForm = document.querySelector("#loginForm");
const rootLoginForm = ReactDOM.createRoot(domContainerLoginForm);
rootLoginForm.render(createLoginForm(LoginForm));
