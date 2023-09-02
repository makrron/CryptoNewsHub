import axios from 'axios';
export const getAllNews = () => {
  return axios.get('http://127.0.0.1:8000/news/api/v1/news/');
}

// function to get news ordered by date
export const getNewsByDate = () => {
  return axios.get('http://127.0.0.1:8000/news/api/v1/news/?ordering=-date');
}