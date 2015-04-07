################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
O_SRCS += \
../src/add.o \
../src/add_wrap.o 

C_SRCS += \
../src/add.c \
../src/rgrow.c \
../src/rgrow_wrap.c 

OBJS += \
./src/add.o \
./src/rgrow.o \
./src/rgrow_wrap.o 

C_DEPS += \
./src/add.d \
./src/rgrow.d \
./src/rgrow_wrap.d 


# Each subdirectory must supply rules for building sources it contributes
src/%.o: ../src/%.c
	@echo 'Building file: $<'
	@echo 'Invoking: GCC C Compiler'
	gcc -I/usr/include/c++/4.9 -I/usr/include/x86_64-linux-gnu -I/usr/include/x86_64-linux-gnu/c++/4.9/bits -I/usr/include/x86_64-linux-gnu/c++/4.9/bits/ -O0 -g3 -Wall -c -fmessage-length=0 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@:%.o=%.d)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


