const togg = document.getElementById('toggle')
const navActive = document.querySelector('.active')
const labels = document.querySelectorAll('label')

/********FORM*********************** */

labels.forEach(label => {
    label.innerHTML = label.innerText
    .split('')
    .map((letter, idx) => `<span style="transition-delay:${idx * 50}ms">${letter}</span>`)
    .join('')
})



/*************Nav***************** */


togg.addEventListener('click', () => {
    //console.log("button clicked")
    navActive.classList.toggle('active');
});



/*************Generate plans***************** */
document.getElementById('generatePlanButton').addEventListener('click', () => {
    window.location.href = "{{ url_for('main.generate_plans') }}";
});
//navActive.addEventListener('click', () =>{
    //console.log('clicked')
//})