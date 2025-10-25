package com.trancendos.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.http.ResponseEntity;

/**
 * Transaction Controller for handling financial operations.
 * 
 * @author Trancendos Team
 * @version 1.0
 * @since 2025-10-25
 */
@RestController
@RequestMapping("/api/transactions")
public class TransactionController {

    /**
     * Get all transactions.
     * 
     * @return ResponseEntity with transaction list
     */
    @GetMapping
    public ResponseEntity<String> getAllTransactions() {
        return ResponseEntity.ok("Transactions retrieved successfully");
    }

    /**
     * Create new transaction.
     * 
     * @param transactionData the transaction data
     * @return ResponseEntity with creation status
     */
    @PostMapping
    public ResponseEntity<String> createTransaction(@RequestBody String transactionData) {
        return ResponseEntity.ok("Transaction created successfully");
    }

    /**
     * Health check endpoint.
     * 
     * @return ResponseEntity with health status
     */
    @GetMapping("/health")
    public ResponseEntity<String> healthCheck() {
        return ResponseEntity.ok("Transaction service is healthy");
    }
}