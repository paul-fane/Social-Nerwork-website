document.addEventListener('DOMContentLoaded', function() {

    // Edit button
    const editButtons = document.querySelectorAll('.edit');
    editButtons.forEach(button => {editButton(button)});

    // Follow button
    const followButton = document.querySelector('#follow-butoon');
    if (followButton){
        followButton.addEventListener('click', load_button);
    }

    // Like button
    const likeButtons = document.querySelectorAll('.like');
    likeButtons.forEach(button => {likeButton(button)});

    // Show comment
    const showComments = document.querySelectorAll('.comment');
    showComments.forEach(button =>{showComment(button)});

    // Add comment
    const addComments = document.querySelectorAll('.write-comment');
    addComments.forEach(post =>{addComment(post)});

    // Search user
    const inputSearch = document.querySelector('#search-user');
    inputSearch.addEventListener('input', fetchUser);

    // Show likes list in modal
    const likesList = document.querySelectorAll('.likesList');
    likesList.forEach( like => {showLikeList(like)} );

    // Show followers list in modal
    const followersList = document.querySelectorAll('.followers');
    followersList.forEach(profile => {showFollowersList(profile)});

    // Show following list in modal
    const followingList = document.querySelectorAll('.following');
    followingList.forEach(profile => {showFollowingList(profile)});

    // Fetch profile image
    const fetchImages = document.querySelectorAll('.profile-image');
    fetchImages.forEach(post => {fetchImage(post)});

    // Fetch profile image for comments
    const commentImage = document.querySelectorAll('.profile-image-comment');
    commentImage.forEach(post => {fetchCommentImage(post)});
});


function load_button(){
    // Select the follow button
    const followButton = document.querySelector('#follow-butoon');
    // Select the username that contain the user data
    const username = document.querySelector('#username');
    // Get the cookie
    let csrftoken = getCookie('csrftoken');

    // Fetch the relationship between curent user and profile
    fetch(`/follow-button/${username.dataset.profile}`)
    .then(response => response.json())
    .then(data => {
        
        // Check if there is relationship
        if (data.relation === true){
            // If there is relation the button will remuve the relation 
            fetch('/removefollow', {
                method: 'PUT',
                body: JSON.stringify({profileUser: username.dataset.profile}),
                headers: {"X-CSRFToken": csrftoken}
            })
            .then(response => response.json())
            .then(data => {

                // Update the number of followers
                document.querySelector('#num-followers').innerHTML=`${data['numFollowers']} Followers`;

                // Change the button to follow, if want to follow again
                followButton.innerHTML = "Follow";
            })
            .catch(err => {
                console.log(err);
            });
        } else {
            // If there is not a relation the button will add the relation
            fetch('/addfollow', {
                method: 'PUT',
                body: JSON.stringify({
                    profileUser: username.dataset.profile
                }),
                headers: {"X-CSRFToken": csrftoken}
            })
            .then(response => response.json())
            .then(data => {

                // Update the number of followers
                document.querySelector('#num-followers').innerHTML=`${data['numFollowers']} Followers`;

                // Change the button to unfollow, if want to unfollow again
                followButton.innerHTML = "Unfollow";
            })
            .catch(err => {
                console.log(err)
            });
        }
    })
    .catch(err => {
        console.log(err)
    });
}


function editButton(button){
    button.addEventListener('click', ()=>{
        const postid = button.dataset.postid;
        button.style.display = 'none';

        let csrftoken = getCookie('csrftoken');
        
        // Select the content
        let content = document.querySelector(`#content${postid}`);

        // Set the form for edit with the old content pre-filled
        // Name the class whithout the "white-space" CSS proprety
        content.className = "card-text";
        content.innerHTML =
            `<form id="edit-form" class="form-tweet">
                <textarea id="edit-textarea" autofocus class="form-control" rows="3">${content.innerHTML}</textarea>
                <button class="btn btn-primary" type="submit">Save</button>
            </form>`
        
        // When submit the form
        document.querySelector('#edit-form').onsubmit = () => {
            const newContent = document.querySelector('#edit-textarea').value;
            
            // Send edit content to the server
            fetch('/editcontent', {
                method: 'PUT',
                body: JSON.stringify({newContent, postid}),
                headers: {"X-CSRFToken": csrftoken}
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    console.log(`Error editing post: ${data.error}`);
                } else {
                    // Set the new content on the client side
                    content.innerHTML = newContent;
                    button.style.display = 'block';
                }
            })
            .catch(err => {
                console.log(err);
            })
            // Put "white-space" CSS proprety back
            content.className = "card-text white-space";
            return false;
        }
    }); 
}


// Function from: https://www.stackhawk.com/blog/django-csrf-protection-guide/
function getCookie(name) {
    let cookieValue = null;

    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();

            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));

                break;
            }
        }
    }

    return cookieValue;
}


function likeButton(button){
    button.addEventListener('click', ()=>{
        const postid = button.dataset.postid;
        
        let csrftoken = getCookie('csrftoken');
        //button.style.display = 'none';
        
        // Send like
        fetch('/like', {
            method: 'PUT',
            body: JSON.stringify({postid}),
            headers: {"X-CSRFToken": csrftoken}
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.log(`Error likeing post: ${data.error}`);
            } else {
                if (data.addlike === true){
                    // Set the image and the number of likes
                    document.querySelector(`#like${postid}`).setAttribute('src', 'static/red-heart.svg');
                    document.querySelector(`#num-like${postid}`).innerHTML = `${data.numlike} like/s`;
                    
                } else {
                    // Set the image and the number of likes
                    document.querySelector(`#like${postid}`).setAttribute('src', 'static/heart.svg');
                    document.querySelector(`#num-like${postid}`).innerHTML = `${data.numlike} like/s`;
                    
                }
                
            }
        })
        .catch(err => {
            console.log(err);
        })
        return false;
    });
}


function showComment(button){
    button.addEventListener('click', ()=>{
        const postid = button.dataset.postid;
        // When the button is pressed, show the div container of form to add a comment and comments
        document.querySelector(`#comment${postid}`).style.display = 'block';
    });
}


function addComment(post){
    const postid = post.dataset.postid;
    let csrftoken = getCookie('csrftoken');

    // Select the submit button and input to be used later
    const submit = document.querySelector(`#submit${postid}`);
    const input = document.querySelector(`#write-comment-${postid}`);

    // Disable submit button by default:
    submit.disabled = true;

    // Listen for input to be typed into the input field
    input.onkeyup = () => {
        if (input.value.length > 0) {
            submit.disabled = false;
        }
        else {
            submit.disabled = true;
        }
    }

    post.onsubmit = ()=>{
        const newComment = input.value;

        // Send the comment to server and append the comment
        fetch('/comments', {
            method: 'POST',
            body: JSON.stringify({newComment, postid}),
            headers: {"X-CSRFToken": csrftoken}
        })
        .then(response => response.json())
        .then(result => {
            if (result.error) {
                // Print error
                console.log(`Error commenting post: ${data.error}`);
            }else {
                if (result.image === "noImage"){
                    // Create the conteiner of username and comment
                    const commentContainer = document.createElement('div');
                    commentContainer.className = "comment-container border top-card";
                    commentContainer.idName = `comment-container-${postid}`;
                    commentContainer.innerHTML = `
                        <div class="profile-image-comment" id="profile-image-{{comment.id_user}}{{comment.id}}" data-commentid="{{comment.id}}" data-iduser="{{comment.id_user}}">
                        <img src="/../../static/default-profile.png" class="rounded-circle card-img" width="15px" alt="...">
                        </div>
                        <div>
                            <a class="a-tag" href="/profile-${result.currentUser.username}">${result.currentUser.username}</a>
                            <div>${newComment}</div>
                        </div>`;

                    // Append the new comment to the end of all comments
                    document.querySelector(`#comment${postid}`).append(commentContainer);

                    // Update the number of comments
                    const numberComments = document.querySelector(`#number-comments-${postid}`);
                    numberComments.innerHTML = `${result.numberComments} comments`;

                    // Clear out input field:
                    input.value = '';

                    // Disable the submit button again:
                    submit.disabled = true;
                } else {
                    // Create the conteiner of username and comment
                    const commentContainer = document.createElement('div');
                    commentContainer.className = "comment-container border top-card";
                    commentContainer.idName = `comment-container-${postid}`;
                    commentContainer.innerHTML = `
                        <div class="profile-image-comment" id="profile-image-{{comment.id_user}}{{comment.id}}" data-commentid="{{comment.id}}" data-iduser="{{comment.id_user}}">
                        <img src="/../../../media/${result.image}" class="rounded-circle card-img" width="15px" alt="...">
                        </div>
                        <div>
                            <a class="a-tag" href="/profile-${result.currentUser.username}">${result.currentUser.username}</a>
                            <div>${newComment}</div>
                        </div>`;

                    // Append the new comment to the end of all comments
                    document.querySelector(`#comment${postid}`).append(commentContainer);

                    // Update the number of comments
                    const numberComments = document.querySelector(`#number-comments-${postid}`);
                    numberComments.innerHTML = `${result.numberComments} comments`;

                    // Clear out input field:
                    input.value = '';

                    // Disable the submit button again:
                    submit.disabled = true;
                }
                
                
            }
        })
        .catch(err => {
            console.log(err);
        });
        // Stop form from submitting
        return false;
    }
}


function fetchUser(){
    const inputSearch = document.querySelector('#search-user');
    //Clean old "a" tag content
    document.querySelector('.dropdown-content').innerHTML = '';
    if (inputSearch.value.length > 0){

        //Show the resul
        document.querySelector("#myDropdown").style.display = 'block';

        //fetch the user
        fetch(`/search/${inputSearch.value}`)
        .then(response => response.json())
        .then(persons => {
            for (const person of persons){
                // For every user creat an "a" tag whit his name and if click => redirect to his profile
                const element = document.createElement('a')
                element.innerHTML = `${person['username']}`;
                element.setAttribute("href", `profile-${person["username"]}`);
                document.querySelector('.dropdown-content').append(element);

            }
        })
        .catch(err => {
            console.log(err);
        });
    } else if (inputSearch.value.length < 1) {
        //Hide the empty result
        document.querySelector("#myDropdown").style.display = 'none';
        
    }
}

function showLikeList(like){
    like.addEventListener('click', ()=>{

        //fetch the likes
        fetch(`/likesList/${like.dataset.postid}`)
        .then(response => response.json())
        .then(likes => {
            // Delete the old list of likes in the modal (if any)
            const list = document.querySelector(`#modal-likes-${like.dataset.postid}`);

            while (list.hasChildNodes()) {
            list.removeChild(list.firstChild);
            }

            // New list
            for (user of likes.person){
                // Select the modal of the actual post
                const element = document.createElement('p')
                element.innerHTML = `<a class="a-tag" href="/profile-${user.username}">${user.username}</a>`;
                list.append(element);
            }
        })
        .catch(err => {
            console.log(err);
        });
    });
}

function showFollowersList(profile){
    profile.addEventListener('click', ()=>{

        //fetch the followers
        fetch(`/followersList/${profile.dataset.profile}`)
        .then(response => response.json())
        .then(followers => {
            // Delete the old list of followers in the modal (if any)
            const list = document.querySelector(`#modal-followers-${profile.dataset.profile}`);

            while (list.hasChildNodes()) {
            list.removeChild(list.firstChild);
            }

            // New list
            for (user of followers){
                // Select the modal of the actual post
                const element = document.createElement('p')
                element.innerHTML = `<a class="a-tag" href="/profile-${user.username}">${user.username}</a>`;
                list.append(element);
            }
        })
        .catch(err => {
            console.log(err);
        });
    });
}


function showFollowingList(profile){
    profile.addEventListener('click', ()=>{

        //fetch the following
        fetch(`/followingList/${profile.dataset.profile}`)
        .then(response => response.json())
        .then(following => {
            // Delete the old list of following in the modal (if any)
            const list = document.querySelector(`#modal-following-${profile.dataset.profile}`);

            while (list.hasChildNodes()) {
            list.removeChild(list.firstChild);
            }

            // New list
            for (user of following){
                // Select the modal of the actual post
                const element = document.createElement('p')
                element.innerHTML = `<a class="a-tag" href="/profile-${user.username}">${user.username}</a>`;
                list.append(element);
            }
        })
        .catch(err => {
            console.log(err);
        });
    });
}


function fetchImage(post){
    const profileImage = document.querySelector(`#profile-image-${post.dataset.iduser}${post.dataset.postid}`);
    if (profileImage.hasChildNodes() === false){
        //fetch the image
        fetch(`/image/${post.dataset.iduser}`)
        .then(response => response.json())
        .then(image => {
            if (image.image === "noImage"){
                // Create default image
                console.log(image.image);
                const img = document.createElement('img');
                img.src = '../../static/default-profile.png';
                img.className = "rounded-circle card-img";
                profileImage.appendChild(img);
            } else {
                // Create profile image
                console.log(image.image);
                const img = document.createElement('img');
                img.src = `../../../media/${image.image}`;
                img.className = "rounded-circle card-img";
                profileImage.appendChild(img);
            }
        })
        .catch(err => {
            console.log(err);
        });
    }
}


function fetchCommentImage(post){
    const commentImage = document.querySelector(`#profile-image-${post.dataset.iduser}${post.dataset.commentid}`);
    if (commentImage.hasChildNodes() === false){
        //fetch the image
        fetch(`/comment-image/${post.dataset.iduser}`)
        .then(response => response.json())
        .then(image => {
            if (image.image === "noImage"){
                // Create default image
                console.log(image.image);
                const img = document.createElement('img');
                img.src = '../../static/default-profile.png';
                img.className = "rounded-circle card-img";
                commentImage.appendChild(img);
            } else {
                // Create profile image
                console.log(image.image);
                const img = document.createElement('img');
                img.src = `../../../media/${image.image}`;
                img.className = "rounded-circle card-img";
                commentImage.appendChild(img);
            }
        })
        .catch(err => {
            console.log(err);
        });
    }
}