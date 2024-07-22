document.addEventListener('DOMContentLoaded', function() {
    const addButton = document.querySelector('.control-button.add');
    const removeButton = document.querySelector('.control-button.remove');
    const form = document.getElementById('search-form');

    addButton.addEventListener('click', () => {
        const searchGroup = document.createElement('div');
        searchGroup.classList.add('search-group');
        searchGroup.innerHTML = `
            <select title="Boolean Operator">
                <option value="AND">AND</option>
                <option value="OR">OR</option>
                <option value="NOT">NOT</option>
            </select>
            <input type="text" placeholder="Search Term">
            <select title="Select Metadata">
                <option>abstract</option>
                <option>IEEE keywords</option>
                <option>DOI</option>
                <option>Title</option>
            </select>
        `;
        document.querySelector('form').insertBefore(searchGroup, document.querySelector('.search-controls'));
    });

    removeButton.addEventListener('click', () => {
        const searchGroups = document.querySelectorAll('.search-group');
        if (searchGroups.length > 1) {
            searchGroups[searchGroups.length - 1].remove();
        }
    });

    form.addEventListener('submit', function(event) {
        event.preventDefault();
        const searchGroups = document.querySelectorAll('.search-group');
        let kibanaQuery = '';
        let query = {
            must: [],
            should: [],
            must_not: [], 
        }
        searchGroups.forEach((group, index) => {
            let operator = group.querySelector('select:first-of-type').value;
            const searchTerm = group.querySelector('input').value.trim();
            let metadata = group.querySelector('select:last-of-type').value;
            if (index == 0 || operator === "AND") {
                operator = "must"
            }
            else if (operator === "OR") {
                operator = "should"
            }
            else if (operator === "NOT") {
                operator= "must_not"
            }
            if (searchTerm && searchTerm.trim() !== "") {
                query[operator].push({
                    "match": {
                        [metadata]: searchTerm
                    }
                });
            }
        });
        Object.keys(query).forEach((key)=> {
            if(query[key].length === 0){
                delete query[key]
            }
        })
        fetch('http://127.0.0.1:3000/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(query)
        })
    });
});
