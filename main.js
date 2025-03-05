const fetch = require('node-fetch');
const fs = require('fs');

const url = 'https://cloudcomputingclub.co.in/api/registrations';

fetch(url)
  .then(response => response.json())
  .then(jsonData => {
    if (!jsonData || !jsonData.registrationDetails) {
      throw new Error('Invalid API response: Missing registrationDetails');
    }

    const extractedData = {
      rollno: jsonData.registrationDetails?.rollno || 'N/A',
      name: jsonData.name || 'N/A',
      phone: jsonData.registrationDetails?.phone || 'N/A',
      email: jsonData.email || 'N/A'
    };

    fs.writeFile('dataset.json', JSON.stringify(extractedData, null, 2), (err) => {
      if (err) throw err;
      console.log('Data has been saved to dataset.json');
    });
  })
  .catch(error => {
    console.error('Error fetching data:', error.message);
  });
