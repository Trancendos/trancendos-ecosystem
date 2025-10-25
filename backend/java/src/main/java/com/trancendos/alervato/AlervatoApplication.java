package com.trancendos.alervato;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.data.jpa.repository.config.EnableJpaAuditing;

/**
 * The main entry point for the Alervato application.
 * <p>
 * This class initializes and runs the Spring Boot application.
 *
 * @author Trancendos
 * @version 1.0
 */
@SpringBootApplication
@EnableJpaAuditing
public class AlervatoApplication {

	/**
	 * The main method that starts the Alervato application.
	 *
	 * @param args Command-line arguments passed to the application.
	 */
	public static void main(String[] args) {
		SpringApplication.run(AlervatoApplication.class, args);
	}
}
