package com.trancendos.alervato.controller;

import com.trancendos.alervato.dto.TransactionDTO;
import com.trancendos.alervato.model.Transaction;
import com.trancendos.alervato.service.TransactionService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/transactions")
@CrossOrigin(origins = "*")
public class TransactionController {

    @Autowired
    private TransactionService transactionService;

    @GetMapping
    public ResponseEntity<Page<Transaction>> getUserTransactions(
            Authentication authentication,
            Pageable pageable) {
        String username = authentication.getName();
        Page<Transaction> transactions = transactionService.getUserTransactions(username, pageable);
        return ResponseEntity.ok(transactions);
    }

    @PostMapping
    public ResponseEntity<?> createTransaction(
            @Valid @RequestBody TransactionDTO transactionDTO,
            Authentication authentication) {
        try {
            String username = authentication.getName();
            Transaction transaction = transactionService.createTransaction(transactionDTO, username);
            return ResponseEntity.ok(transaction);
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(e.getMessage());
        }
    }

    @GetMapping("/{id}")
    public ResponseEntity<?> getTransaction(
            @PathVariable Long id,
            Authentication authentication) {
        try {
            String username = authentication.getName();
            Transaction transaction = transactionService.getTransactionById(id, username);
            return ResponseEntity.ok(transaction);
        } catch (Exception e) {
            return ResponseEntity.notFound().build();
        }
    }

    @PutMapping("/{id}")
    public ResponseEntity<?> updateTransaction(
            @PathVariable Long id,
            @Valid @RequestBody TransactionDTO transactionDTO,
            Authentication authentication) {
        try {
            String username = authentication.getName();
            Transaction transaction = transactionService.updateTransaction(id, transactionDTO, username);
            return ResponseEntity.ok(transaction);
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(e.getMessage());
        }
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<?> deleteTransaction(
            @PathVariable Long id,
            Authentication authentication) {
        try {
            String username = authentication.getName();
            transactionService.deleteTransaction(id, username);
            return ResponseEntity.ok().body("Transaction deleted successfully");
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(e.getMessage());
        }
    }
}