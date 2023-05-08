const tableBody = document.querySelector('#data-table tbody');
fetch('Paper List for Portal - Sheet1.csv')
  .then(response => response.text())
  .then(data => {
    const jsonData = Papa.parse(data, { header: true, skipEmptyLines: true }).data;

    jsonData.forEach(row => {
      const author = row['Authors']
      const title = row['Title'];
      const abstract = row['TL;DR (generated using GPT)'];
      const link = row['Link'];
      const github = row['Github'];
      const publication_conference = row['Publication Conference'];

      // Create the container element
      const container = document.createElement('div');
      container.classList.add('container', 'blur', 'p-5');

      // Create the title element
      const titleElement = document.createElement('h4');
      titleElement.textContent = title;
      titleElement.classList.add('paper-title', "col-md-12");
      container.appendChild(titleElement);

      // Create the element to add above abstractAndImageRow
      const authorElement = document.createElement('div');
      authorElement.textContent = author;
      authorElement.classList.add('authors', 'col-md-12')
      container.appendChild(authorElement);

      container.appendChild(document.createElement('br'));

      // Create the publication conference element
      const publicationConferenceElement = document.createElement('div');
      publicationConferenceElement.textContent = publication_conference
      publicationConferenceElement.classList.add("conference")

      // Create the row element for the abstract and publication conference
      const abstractRow = document.createElement('div');
      abstractRow.classList.add('row', 'col-md-6');

      // abstractRow.appendChild(authorElement)
      abstractRow.appendChild(publicationConferenceElement)

      // Create the abstract element
      const abstractElement = document.createElement('p');
      abstractElement.classList.add('text-justify');
      abstractElement.style.color = 'white';
      abstractElement.innerHTML = `<strong style="color: #D4AC0D;"></strong>${abstract}`;
      abstractRow.appendChild(abstractElement);

      // Create the row element for the links
      const linksRow = document.createElement('div');
      linksRow.classList.add('row', 'col-md-12', 'text-left');

      // Create the paper link element
      const paperLinkElement = document.createElement('a');
      paperLinkElement.href = link;
      paperLinkElement.target = '_blank';
      paperLinkElement.textContent = '[Paper]';
      paperLinkElement.style.color = '#D4AC0D';
      paperLinkElement.style.fontWeight = 'bold';
      paperLinkElement.classList.add('mr-2', 'hover');
      linksRow.appendChild(paperLinkElement);

      // Create the code link element
      if (github) {
        const codeLinkElement = document.createElement('a');
        codeLinkElement.href = github;
        codeLinkElement.target = '_blank';
        codeLinkElement.textContent = '[Code]';
        codeLinkElement.style.color = '#D4AC0D';
        codeLinkElement.style.fontWeight = 'bold';
        codeLinkElement.classList.add('mr-2', 'ml-3', 'hover');
        linksRow.appendChild(codeLinkElement);
      }

      abstractRow.appendChild(linksRow);
      // Create the image element
      const imageCol = document.createElement('div')
      imageCol.classList.add('col-md-5', 'img-fluid')
      const imageElement = document.createElement('img');
      imageElement.classList.add('img-fluid', 'paper-image', 'align-middle');
      imageElement.src = `./papersImages/${title}.png`;
      //   umang: this distorts the images; don't do this
      //   imageElement.style.width = '600px'; // Set a fixed width
      //   imageElement.style.height = '250px'; // Set a fixed height

      // Add event listener to check if image loaded successfully
      imageElement.addEventListener('error', function () {
        // If image is unavailable, display nothing
        imageElement.style.display = 'none';
      });
      imageCol.appendChild(imageElement)

      // Create the element to add above abstractAndImageRow
      const margin_md = document.createElement('div');
      // aboveRow.textContent = 'Content above the abstract and image row';
      margin_md.classList.add('col-md-1');
      // margin_md.style.marginBottom = '10px';

      // Create the parent row element for the abstract and image
      const abstractAndImageRow = document.createElement('div');
      abstractAndImageRow.classList.add('row');
      //   https://stackoverflow.com/questions/37156582/bootstrap-vertical-align-image
      abstractAndImageRow.classList.add('d-flex', 'flex-wrap', 'align-items-center');

      // Append the aboveRow, abstract and image elements to the parent container
      //   container.appendChild(aboveRow);
      //   container.appendChild(publicationConferenceElement)
      container.appendChild(abstractAndImageRow);
      abstractAndImageRow.appendChild(abstractRow);
      abstractAndImageRow.appendChild(margin_md);
      abstractAndImageRow.appendChild(imageCol);

      // Append the container to the table body
      tableBody.appendChild(container);
      tableBody.appendChild(document.createElement('br'));
    });

    return jsonData;
  })
  .catch(error => console.error(error));

// blinking arrow
var arrowContainer = document.querySelector('.arrow-container');
var arrowVisible = true;
var scrollThreshold = 100;

window.addEventListener('scroll', function () {
  var scrolled = window.scrollY;

  if (scrolled > scrollThreshold && arrowVisible) {
    arrowContainer.style.opacity = '0';
    arrowContainer.style.pointerEvents = 'none';
    arrowVisible = false;
  } else if (scrolled <= scrollThreshold && !arrowVisible) {
    arrowContainer.style.opacity = '1';
    arrowContainer.style.pointerEvents = 'auto';
    arrowVisible = true;
  }
});