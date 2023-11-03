'use strict';

const build = React.createElement;
const userInfo = document.getElementById("userdata").value;
const votacionParticipo = document.getElementById("hide").value;
const dicc = JSON.parse(votacionParticipo);

const view = [];
const keys = Object.keys(dicc);

for(let i = 0; i < keys.length; i++){
    const id= keys[i];
    const lista = dicc[id];
    const name = lista[1];
    const desc = lista[2];
    const publico = lista[3].toString();

    const aux = build ("tr", {key: i}, 
                    build("td",{key: "id", className: "tablebody"},id),
                    build("td",{key: "name", className: "tablebody"},name),
                    build("td",{key: "desc", className: "tablebody"},desc),
                    build("td",{key: "public", className: "tablebody"},publico),
                    build("td", { key: "button" },
                        build("button",{},
                            build("a",{href:"/booth/".concat(id)}, "Go Vote"),                 
                        ),
                        build("button",{},
                            build("a", { href: "/census/deleteUser/".concat(id) }, "Quit Census")                 
                        )
                    )                  
    );
    view.push(aux)
}
class List extends React.Component {
    render (){
        
        if((userInfo != "AnonymousUser")){
        return build("table", {},
                build("thead", {},
                    build("tr",{},
                        build("td", {className: "tableHead"}, "ID"),
                        build("td", {className: "tableHead"}, "Name"),
                        build("td", {className: "tableHead"}, "Description"),
                        build("td", {className: "tableHead"}, "Public"),
                        build("td", {className: "tableHead"}, "Actions"),
                    )    
                ),
                build("tbody",{},view));   
        }else {
            return build(
                "div", {},
                build("h1", {className: "Title"}, "If you want to see this service you need to log in"),
                
            );
        }
    }
}    

const domContainerBody = document.querySelector('#list');
const rootBody = ReactDOM.createRoot(domContainerBody);
rootBody.render(build(List));