
// простой скрипт для проверки работы JS. Он выводит в консоль поля name и email, на старнице "расписания"
// в форме регистрации.
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');

    form.addEventListener('submit', function(event) {
        event.preventDefault();

        const name = document.getElementById('name').value;
        const email = document.getElementById('email').value;

        console.log('Имя:', name);
        console.log('Email:', email);
    });
});
