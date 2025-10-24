package com.trancendos.alervato;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.data.jpa.repository.config.EnableJpaAuditing;

@SpringBootApplication
@EnableJpaAuditing
public class AlерваtoApplication {
	public static void main(String[] args) {
		SpringApplication.run(AlерваtoApplication.class, args);
	}
}