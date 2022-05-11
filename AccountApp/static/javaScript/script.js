let hamburger = document.getElementById('hamburger')
let nav_menu = document.getElementById('menu')
let counter1 = false

let kategori_menu = document.getElementById('kategori_tarih_menu')
let kategori_menu_icon = document.getElementById('kategori_tarih_menu_icon')
let counter2 = false

let profil_menu = document.getElementById('profil_menu')
let uyelik_menu = document.querySelector('.uyelik')
let counter3 = false ;

if (hamburger){
    hamburger.addEventListener('click',function(){
        if(!counter1){//n. Basış
            nav_menu.style.display='flex'
            counter1=true
        }
        else if(counter1){//2n.inci basış
            nav_menu.style.display='none'
            counter1=false
        }
    })
}

if(kategori_menu_icon){
    kategori_menu_icon.addEventListener('click' , function(){
        if(!counter2){//n. Basış
            kategori_menu.style.display='block'
            counter2=true
        }
        else if(counter2){//2n.inci basış
            kategori_menu.style.display='none'
            counter2=false
        }
    })
}

if(uyelik_menu){
    uyelik_menu.addEventListener('click',function () {
        if(!counter3){
            profil_menu.classList.add('profil_menu_aktif')
            counter3=true
        }
        else{
            profil_menu.classList.remove('profil_menu_aktif')
            counter3=false
        }
    })
}