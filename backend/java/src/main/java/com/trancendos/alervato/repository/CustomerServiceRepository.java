package com.trancendos.alervato.repository;

import com.trancendos.alervato.model.CustomerService;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

/**
 * Repository for the CustomerService entity.
 */
@Repository
public interface CustomerServiceRepository extends JpaRepository<CustomerService, Long> {
}
