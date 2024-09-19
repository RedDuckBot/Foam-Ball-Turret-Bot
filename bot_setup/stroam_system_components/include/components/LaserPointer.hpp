#ifndef LASER
#define LASER

#include "libgpio/DigitalOutput.hpp"

namespace Components
{
    class LaserPointer
    {
    	public:
            LaserPointer(uint32_t gpioPin);

            void on();
            void off();

        private:
	    libgpio::DigitalOutput laserPin_;
    };
}
#endif 
