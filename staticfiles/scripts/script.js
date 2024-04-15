let sidebar = document.querySelector(".sidebar");
let closeBtn = document.querySelector("#btn");
let icon = document.getElementById("logo_sgabs")



closeBtn.addEventListener("click", ()=>{
  sidebar.classList.toggle("open");

  menuBtnChange();//calling the function(optional)
});


// following are the code to change sidebar button(optional)
function menuBtnChange() {
 if(sidebar.classList.contains("open")){
   closeBtn.classList.replace("bx-menu", "bx-menu-alt-right");//replacing the iocns class
   icon.classList.replace("hide", "logo_display")
 }else {
   closeBtn.classList.replace("bx-menu-alt-right","bx-menu");//replacing the iocns class
      icon.classList.replace("logo_display", "hide")
 }
}
