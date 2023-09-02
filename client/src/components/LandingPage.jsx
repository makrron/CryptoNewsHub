// LandingPage.jsx

import React from 'react';
import Slider from 'react-slick';
import 'slick-carousel/slick/slick.css';
import 'slick-carousel/slick/slick-theme.css';
export function LandingPage() {
    const carousel = [
      {
        id: 1,
        title: 'Stay Informed',
        description: 'Get the latest news and updates on cryptocurrency and blockchain technology.',
      },
      {
        id: 2,
        title: 'Customize Your News',
        description: 'Filter news by categories and sources to see what matters most to you.',
      },
      {
        id: 3,
        title: 'Responsive Design',
        description: 'Enjoy a seamless browsing experience on both desktop and mobile devices.',
      },
      {
        id: 4,
        title: 'Explore Diverse Sources',
        description: 'Access news from a wide range of reputable cryptocurrency sources, including financial publications.',
      },
      {
        id: 5,
        title: 'User-Friendly Interface',
        description: 'Navigate our intuitive interface with ease, whether you are a crypto novice or expert.',
      },
    ];

  // Configuración del carrusel
  const settings = {
    dots: true,
    infinite: true,
    speed: 600,
    slidesToShow: 3,
    slidesToScroll: 1,
  };

  return (
    <div className="bg-gray-100 min-h-screen mt-16"> {/* Agregar la clase mt-16 para dar margen superior */}
      <header className="bg-blue-500 text-white py-8">
        <div className="container mx-auto text-center">
          <h1 className="text-4xl font-semibold">Welcome to CryptoNews</h1>
          <p className="mt-4 text-lg">
            Your source for the latest cryptocurrency news and updates.
          </p>
        </div>
      </header>
    <section className="container mx-auto p-8">
        <Slider {...settings}>
          {carousel.map(c => (
            <div key={c.id}>
              <div className="bg-white p-4 shadow-md rounded-lg h-full flex flex-col justify-between">
                <h3 className="text-lg font-semibold">{c.title}</h3>
                <p className="text-gray-600">{c.description}</p>
              </div>
            </div>
          ))}
        </Slider>
      </section>
      <section className="container mx-auto p-8">
        <h2 className="text-2xl font-semibold mb-4">Why Choose Us?</h2>
        <p className="text-gray-700">
          - Comprehensive Coverage: We provide comprehensive coverage of the cryptocurrency and blockchain space so you don't miss any critical developments or market trends.
        </p>
        <p className="text-gray-700">
            - Real-Time Updates: Stay up-to-date with real-time news and market data, ensuring you're always aware of the latest price movements and breaking news.
        </p>
        <p className="text-gray-700">
            - User-Centric Experience: Our platform is designed with your needs in mind. Enjoy a user-friendly interface, customizable news feeds, and responsive design on any device.
        </p>
        <p className="text-gray-700">
            - Trusted Sources: We curate news from trusted sources, including prominent financial publications, blockchain experts, and cryptocurrency enthusiasts.
        </p>
      </section>
    </div>
  );
}
