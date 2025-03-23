document.addEventListener('DOMContentLoaded', function() {

    document.querySelectorAll('.edit-button').forEach(element => edit_post(element));

    function edit_post(button) {
        button.addEventListener('click', function() {

            this.style.visibility = 'hidden'
            

            let post = this.parentElement.parentElement
            let content = post.querySelector('.post-content').innerHTML

            let save_button = document.createElement('button')
            save_button.classList.add('save-button')
            save_button.innerHTML = 'Save'
            post.querySelector('p').insertBefore(save_button, this)

            post.querySelector('.post-content').style.display = 'none';

            if (!post.querySelector('textarea')) {
                let editable_area = document.createElement('textarea')
                post.insertBefore(editable_area, post.querySelector('.heart'))
                post.querySelector('textarea').innerHTML = content
            }

            post.querySelector('.save-button').addEventListener('click', function() {

                let new_content = post.querySelector('textarea').value

                if (new_content != '') {
                    post.querySelector('.post-content').innerHTML = new_content
                    post.querySelector('textarea').remove()
                    post.querySelector('.post-content').style.display = 'block'
                    post.querySelector('.save-button').remove()
                    button.style.visibility = 'visible'
                }
            })

            // TODO fetch data to the server

        })
    }
})