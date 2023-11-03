'use strict';

const create = React.createElement;
const user = document.getElementById("userdata").value;
class Navbar extends React.Component {
  render() {
    
    if(user != 'AnonymousUser'){
      return create(
        "header",{},
        create("h1",{className:'Logo'},"Decide Booth"),
        create("nav", {className:"NavBar"},
          create("ul",{className: "nav_links"}, 
            create("li",{},
              create("a",
                {href: "/booth/boothList", className: "Link"}, 
                "Open Votings"
              )),
            create("li",{},
              create("a",
                {href: "/booth/boothListPrivate", className: "Link"},
                "My Votings"
            ))
          )
        ),
        create(
          "a",
          {className:"cta", href: "/authentication/salir"}, 
          create("button",{type: "submit" }, "Log Out"),
        ),
      );
    } else {
      return create(
        "header",{},
        create("h1",{className:"Logo"},"Decide Booth"),
        create('nav', {className:"NavBar"},
          create("ul",{ className: "nav_links" },)
        ),
        create(
          "a",
          {className:"cta", href: "/"}, 
          create('button',{type: "submit" }, "Este es el cambio"),
        ),
      );
    }

    
  }
    
}

const domContainer = document.querySelector('#navbar');
const root = ReactDOM.createRoot(domContainer);
root.render(create(Navbar));
