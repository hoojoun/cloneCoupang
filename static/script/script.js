window.onload=function(){
    const input_id=document.querySelector('input[type=email]')
    const input_pw=document.querySelector('input[type=password]')
    const id_error=document.querySelector('.id_error')
    const pw_error=document.querySelector('.pw_error')
    input_id.addEventListener('click',function(){
        id_error.style.display='block'
    })
    input_pw.addEventListener('click',function(){
        pw_error.style.display='block'
    })
}