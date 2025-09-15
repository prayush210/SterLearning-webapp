let sidebar = document.querySelector(".sidebar");
let closeBtn = document.querySelector("#btn");
let searchBtn = document.querySelector(".bx-search");

closeBtn.addEventListener("click", () => {
    sidebar.classList.toggle("open");
    menuBtnChange();//calling the function(optional)
});

searchBtn.addEventListener("click", () => { // Sidebar open when you click on the search iocn
    sidebar.classList.toggle("open");
    menuBtnChange(); //calling the function(optional)
});

// following are the code to change sidebar button(optional)
function menuBtnChange() {
    if (sidebar.classList.contains("open")) {
        closeBtn.classList.replace("bx-menu", "bx-menu-alt-right");//replacing the iocns class
    } else {
        closeBtn.classList.replace("bx-menu-alt-right", "bx-menu");//replacing the iocns class
    }
}

const verticalMenu = document.querySelector('#sidebar'); // Use querySelector to get the first element with the class 'sidebar'

    const wrapper = document.querySelector('#wrapper');

    // Set minimum height to 100vh if wrapper content is less than full screen height
    if (wrapper.scrollHeight < window.innerHeight) {
        verticalMenu.style.minHeight = "100vh";
    } else {
        // Adjust height based on content height
        verticalMenu.style.minHeight = wrapper.scrollHeight + 100 + "px";
    }

/* TODO: Possibly need to make header responsive for some untested sizes */