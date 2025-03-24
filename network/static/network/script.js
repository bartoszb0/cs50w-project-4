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
                post.insertBefore(editable_area, post.querySelector('.firstspan').nextSibling);
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
    document.querySelectorAll('.heart-liked').forEach(element => handle_like(element));

    function handle_like(element) {
        element.addEventListener('click', function() {

            let like_count = parseInt(element.parentElement.querySelector('.likes').innerHTML)

            let displayed_like = element

            if (!displayed_like.classList.contains('heart-liked')) {
                like_count++
                displayed_like.classList.add('heart-liked')
            } else {
                like_count--
                displayed_like.classList.remove('heart-liked')
                displayed_like.classList.add('heart')
            }
            
            element.parentElement.querySelector('.likes').innerHTML = ` ${like_count}`

            // fetch data to server
            fetch('handlelike', {
                method: 'POST',
                body: JSON.stringify({
                    post_id: element.dataset.postId
                })
            })
        })
    }

    // HANDLE FOLLOW

    let button = document.querySelector('#followButton')

    if (button.innerHTML.trim() === 'UNFOLLOW') {
        button.classList.add('unfollow')
    }

    button.addEventListener('click', function() {

        let followersCount = parseInt(button.parentElement.querySelector('#followersCount').innerHTML)
        
        // change the display of a button
        if (button.innerHTML.trim() === 'UNFOLLOW') {
            button.innerHTML = 'FOLLOW'
            followersCount--
            button.classList.remove('unfollow')
        } else {
            button.innerHTML = 'UNFOLLOW'
            followersCount++
            button.classList.add('unfollow')
        }

        button.parentElement.querySelector('#followersCount').innerHTML = followersCount

        // fetch data to server
        const user = button.dataset.user

        fetch('handlefollow', {
            method: 'POST',
            body: JSON.stringify({
                follow_who: user
            })
        })
    });
})