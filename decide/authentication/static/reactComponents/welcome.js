"use strict";

const createWelcome = React.createElement;

class Welcome extends React.Component {
  render() {
    return createWelcome(
        "body",
        {},
        createWelcome(
          "div",{className:"welcome"},
          createWelcome("br"),
          createWelcome(
            "h2",{className:"h2Welcome"},"Welcome!"),
          createWelcome(
            "p",
            {className:"pWelcome"},
            "To enter admin mode, just click the button!"),
          createWelcome(
            "div",{className:"divWelcomeButton"},
            createWelcome(
              "a",{className:"aWelcome", href: "/admin/"},
              createWelcome(
                "button", {className:"buttonWelcome"} ,"Admin"),
            )
          ),
          createWelcome("br")
        )
    );}
    
}

const domContainerWelcome = document.querySelector("#welcome");
const rootWelcome = ReactDOM.createRoot(domContainerWelcome);
rootWelcome.render(createWelcome(Welcome));
