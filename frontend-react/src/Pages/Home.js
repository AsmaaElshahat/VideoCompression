import '../App.css';
import { useState } from 'react';


function Home() {

  const [name, setName] = useState("");

  const handleSubmit = (event) => {
    event.preventDefault();
    if (!name) {
      alert(`Pleast enter the video link`)
    }
    getVideoLink()
  }

  const getVideoLink = () => {
    const videolink = { name };
    const videoLink = videolink['name']
    return fetch(`http://localhost:8000/upload-video/`,{
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ video_link: videoLink })
    })
    .then(response => response.json())
    .catch(error => console.log(error))
  }

  return (
    <form method='POST' onSubmit={handleSubmit}>
      <label>Video Link:
        <input type="text" name='video_link' value={name} onChange={(e) => setName(e.target.value)} />
      </label>
      <button type='submit'>Upload</button>
    </form>
  );
}

export default Home;