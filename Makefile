ezafeh: kasre_ezafeh.cpp hazm.cpp
	g++ -Wall kasre_ezafeh.cpp hazm.cpp hazm.h -lpython3.10 -o ezafeh $(python3.10-config --ldflags --embed)
