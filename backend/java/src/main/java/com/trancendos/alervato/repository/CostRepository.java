package com.trancendos.alervato.repository;

import com.trancendos.alervato.model.Cost;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

/**
 * Repository for the Cost entity.
 */
@Repository
public interface CostRepository extends JpaRepository<Cost, Long> {
}
