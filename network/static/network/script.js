document.addEventListener('DOMContentLoaded', function() {

    // EDIT POST

    document.querySelectorAll('.edit-button').forEach(element => edit_post(element));

    function edit_post(button) {
        button.addEventListener('click', function() {

            this.style.visibility = 'hidden'

            const postID = this.dataset.postId

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

                    fetch(`saveedit`, {
                        method: 'POST',
                        body: JSON.stringify({
                            edit: new_content,
                            post_id: postID
                        })
                    })
                }
            })

        })
    }


    // HANDLE LIKES

    document.querySelectorAll('.heart').forEach(element => handle_like(element));

    function handle_like(element) {
        element.addEventListener('click', function() {

            console.log('liked')

        })
    }

    // HANDLE FOLLOW

    document.querySelector('#followButton').addEventListener('click', function() {
        const button = this

        const user = button.dataset.user
        console.log(user)

        // change the display of a button
        button.style.backgroundColor = 'white'
        button.style.color = 'black'
        button.style.borderColor = 'black'
        button.innerHTML = 'UNFOLLOW///TODO'

        // increase followers by one or decrease it by one


        // fetch data to server
        fetch(`handlefollow`, {
            method: 'POST',
            body: JSON.stringify({
                follow_who: user
            })
        })
    });
})